import os
import tempfile
import shutil
from pathlib import Path
import textwrap
from urllib.parse import urlparse
import fnmatch

from mcp.server.fastmcp import FastMCP

from .settings import GitExplorerSettings

class GitExplorer:
    """Git Explorer tool for accessing and processing Git repositories."""
    
    def __init__(self, name="Git Codebase Explorer", settings=None):
        """Initialize the Git Explorer with optional custom name and settings."""
        self.mcp = FastMCP(
            name,
            dependencies=["gitpython", "tiktoken"],
        )
        self.settings = settings or GitExplorerSettings()
        
        # Register tools
        self.mcp.tool()(self.get_codebase)
        self.mcp.tool()(self.check_gitlab_token_status)
    
    async def get_codebase(self, repo_url: str, use_token: bool = True) -> str:
        """
        Clone a Git repository and generate a structured text file containing its contents.
        This tool clones a git repository from the provided URL, processes its contents,
        and returns a single text file containing the repository structure and the content
        of all files. Binary files and empty text files are excluded. The tool respects
        .gitignore and .repomixignore patterns. The output includes an estimated token count
        using the o200k_base encoding.
        Args:
            repo_url (str): The URL of the Git repository to clone
            use_token (bool, optional): Whether to use the GitLab token for authentication.
                                       Defaults to True.
        Returns:
            str: A formatted text representation of the repository contents, including
                 file structure, estimated token count, and the content of all text files.
        Raises:
            GitCommandError: If there is an error during the git clone operation
            Exception: For any other errors that occur during processing
        """
        import git
        import tiktoken
        
        authenticated_url = repo_url
        if use_token and self.settings.gitlab_token:
            parsed_url = urlparse(repo_url)
            netloc = f"oauth2:{self.settings.gitlab_token}@{parsed_url.netloc}"
            authenticated_url = parsed_url._replace(netloc=netloc).geturl()
        
        temp_dir = tempfile.mkdtemp()
        try:
            git.Repo.clone_from(authenticated_url, temp_dir, depth=1)
            git_dir = os.path.join(temp_dir, ".git")
            if os.path.exists(git_dir):
                shutil.rmtree(git_dir)
            
            ignore_patterns = []
            gitignore_path = os.path.join(temp_dir, ".gitignore")
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r', errors='replace') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            ignore_patterns.append(line)
            
            repomixignore_path = os.path.join(temp_dir, ".repomixignore")
            if os.path.exists(repomixignore_path):
                with open(repomixignore_path, 'r', errors='replace') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            ignore_patterns.append(line)
            
            repo_structure = self._generate_repo_structure(temp_dir)
            files_content = self._concatenate_files(temp_dir, ignore_patterns)
            
            # Create preamble without token information first
            preamble_base = textwrap.dedent(f"""
            # Git Repository: {repo_url}
            This file contains the complete content of the git repository cloned from:
            {repo_url}
            Below you'll find the repository structure and the full content of all files.
            Each file is preceded by a separator indicating the beginning of the file and
            followed by a separator indicating the end of the file, along with the full path to the file.
            ## Repository Structure:
            {repo_structure}
            ## File Contents:
            """).strip()
            
            # Generate full content
            full_content = f"{preamble_base}\n\n{files_content}"
            
            # Count tokens using tiktoken with o200k_base encoding
            enc = tiktoken.get_encoding("o200k_base")
            tokens = enc.encode(full_content)
            token_count = len(tokens)
            
            # Update preamble with token information
            preamble_with_tokens = textwrap.dedent(f"""
            # Git Repository: {repo_url}
            This file contains the complete content of the git repository cloned from:
            {repo_url}
            Estimated token count (o200k_base encoding): {token_count:,}
            Below you'll find the repository structure and the full content of all files.
            Each file is preceded by a separator indicating the beginning of the file and
            followed by a separator indicating the end of the file, along with the full path to the file.
            ## Repository Structure:
            {repo_structure}
            ## File Contents:
            """).strip()
            
            # Create updated full content
            result = f"{preamble_with_tokens}\n\n{files_content}"
            return result
        except git.GitCommandError as e:
            if "Authentication failed" in str(e):
                return (
                    f"Authentication error while accessing repository {repo_url}.\n"
                    "Make sure the repository is public or a valid access token "
                    "has been set in the GIT_EXPLORER_GITLAB_TOKEN environment variable."
                )
            return f"Git error: {str(e)}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def check_gitlab_token_status(self) -> str:
        """Check if the GitLab token is configured in the environment.
        Returns:
            A message indicating whether the GitLab token is configured
        """
        if self.settings.gitlab_token:
            return "GitLab token is configured."
        else:
            return (
                "GitLab token is not configured. "
                "Set the GIT_EXPLORER_GITLAB_TOKEN environment variable "
                "to access private GitLab repositories."
            )
    
    def run(self, transport: str = "stdio") -> None:
        """Run the Git Explorer with the specified transport."""
        self.mcp.run(transport=transport)
    
    def _should_ignore_file(self, file_path: Path, root_path: Path, ignore_patterns: list[str]) -> bool:
        # Convert to a path relative to the root directory
        rel_path = file_path.relative_to(root_path)
        rel_path_str = str(rel_path).replace(os.sep, '/')
        
        # Check each pattern
        for pattern in ignore_patterns:
            # Handle pattern formats
            if pattern.startswith('/'):
                # Pattern starts with / - only match from root
                pattern = pattern[1:]
                if fnmatch.fnmatch(rel_path_str, pattern):
                    return True
            elif pattern.endswith('/'):
                # Pattern ends with / - match directories
                if file_path.is_dir() and fnmatch.fnmatch(rel_path_str, pattern[:-1]):
                    return True
            else:
                # Standard pattern - match anywhere in path
                if fnmatch.fnmatch(rel_path_str, pattern):
                    return True
                # Also check if any parent directory matches the pattern
                parts = rel_path_str.split('/')
                for i in range(len(parts)):
                    partial_path = '/'.join(parts[:i+1])
                    if fnmatch.fnmatch(partial_path, pattern):
                        return True
        return False
    
    def _generate_repo_structure(self, repo_path: str) -> str:
        result = []
        
        def _add_directory(directory: Path, prefix: str = ""):
            paths = sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name))
            for i, path in enumerate(paths):
                is_last = i == len(paths) - 1
                result.append(f"{prefix}{'└── ' if is_last else '├── '}{path.name}")
                if path.is_dir():
                    _add_directory(
                        path,
                        prefix + ('    ' if is_last else '│   ')
                    )
        
        _add_directory(Path(repo_path))
        return "\n".join(result)
    
    def _is_binary_file(self, file_path: Path) -> bool:
        """Check if a file is binary by reading its first few thousand bytes."""
        try:
            chunk_size = 8000  # Read first 8K bytes
            with open(file_path, 'rb') as f:
                chunk = f.read(chunk_size)
            # Check for null bytes which usually indicate binary content
            if b'\x00' in chunk:
                return True
            # Check if the file is mostly text by looking at the ratio of printable to non-printable characters
            text_characters = bytes(range(32, 127)) + b'\n\r\t\b'
            # If more than 30% non-printable characters, it's likely binary
            return sum(byte not in text_characters for byte in chunk) / len(chunk) > 0.3
        except Exception:
            # If we can't read it, assume it's binary to be safe
            return True
    
    def _concatenate_files(self, repo_path: str, ignore_patterns: list[str]) -> str:
        result = []
        root_path = Path(repo_path)
        
        # Build a list of all files first, so we can sort them
        all_files = []
        for path in sorted(root_path.glob("**/*")):
            if path.is_file():
                all_files.append(path)
        
        for path in all_files:
            if self._should_ignore_file(path, root_path, ignore_patterns):
                continue
            
            # Skip binary files
            if self._is_binary_file(path):
                continue
            
            rel_path = path.relative_to(root_path)
            try:
                # Read file content
                content = path.read_text(errors='replace')
                
                # Skip empty files or files with only empty lines
                if not content or not content.strip():
                    continue
                
                # Add non-empty text file to result
                result.append(f"=====< BEGIN filename: {rel_path} >=====\n")
                result.append(content)
                result.append(f"===== <END filename: {rel_path} >=====\n\n")
            except Exception as e:
                result.append(f"=====< BEGIN filename: {rel_path} >=====\n")
                result.append(f"[Error reading file: {str(e)}]")
                result.append(f"===== <END filename: {rel_path} >=====\n\n")
        
        return "\n".join(result)
