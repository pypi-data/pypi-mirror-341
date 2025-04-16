"""
Aider SDK - Simple Python SDK for using Aider programmatically

This SDK provides an easy way to use Aider, the AI coding assistant,
in your Python scripts without dealing with the underlying complexity.
"""

import os
import json
from typing import List, Dict, Any, Union, Optional


class AiderSDK:
    """
    Main class for interacting with Aider programmatically.

    This SDK allows you to easily use Aider to:
    - Perform AI coding tasks with specific files and prompts
    - List available AI models
    - Work with files in a git repository
    """

    def __init__(
        self,
        working_dir: str,
        model: str = "gemini/gemini-2.5-pro-exp-03-25",
        editor_model: Optional[str] = None,
        use_git: bool = True,
        api_keys: Optional[Dict[str, str]] = None
    ):
        """
        Initialize the Aider SDK.

        Args:
            working_dir: Path to the git repository directory where operations will occur
            model: The AI model to use for coding tasks (default: gemini-2.5-pro-exp-03-25)
            editor_model: Optional separate model for editing operations
            use_git: Whether to use git for tracking changes (default: True)
            api_keys: Dictionary of API keys for various providers, e.g., {"OPENAI_API_KEY": "sk-...", "ANTHROPIC_API_KEY": "sk-..."}
        """
        from aider.models import Model
        from aider.coders import Coder
        from aider.io import InputOutput

        self.working_dir = os.path.abspath(working_dir)
        self.model_name = model
        self.editor_model_name = editor_model
        self.use_git = use_git

        # Set API keys in environment if provided
        if api_keys:
            self._set_api_keys(api_keys)

        # Validate that working_dir is a git repository if use_git is True
        if use_git:
            self._validate_git_repo()

        # Set up the chat history file path
        self.chat_history_file = os.path.join(self.working_dir, ".aider.chat.history.md")

        # Initialize the model
        if editor_model:
            self.model = Model(model=model, editor_model=editor_model)
        else:
            self.model = Model(model)

        # Initialize input/output handler
        self.io = InputOutput(yes=True, chat_history_file=self.chat_history_file)

    def _set_api_keys(self, api_keys: Dict[str, str]):
        """Set API keys as environment variables for Aider to use."""
        # Common API key environment variable names
        supported_keys = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GEMINI_API_KEY",
            "CLAUDE_API_KEY",
            "MISTRAL_API_KEY",
            "FIREWORKS_API_KEY",
            "COHERE_API_KEY",
            "ANYSCALE_API_KEY",
            "OPENROUTER_API_KEY",
            "REPLICATE_API_KEY",
            "TOGETHER_API_KEY",
            "OLLAMA_HOST",
            "GROQ_API_KEY",
        ]

        # Set environment variables for all provided API keys
        for key, value in api_keys.items():
            # Ensure the key is in uppercase format
            env_key = key.upper()
            # If the key doesn't already include "_API_KEY", add it for standard format
            if not env_key.endswith("_API_KEY") and env_key not in ["OLLAMA_HOST"]:
                if "_" not in env_key:
                    env_key = f"{env_key}_API_KEY"

            # Set the environment variable
            os.environ[env_key] = value

        # Log which keys were set (without revealing the actual keys)
        set_keys = [k for k in os.environ.keys() if k in supported_keys]
        if set_keys:
            print(f"Using API keys: {', '.join(set_keys)}")

    def _validate_git_repo(self):
        """Validate that the working directory is a git repository."""
        import subprocess

        try:
            result = subprocess.run(
                ["git", "-C", self.working_dir, "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0 or result.stdout.strip() != "true":
                raise ValueError(
                    f"The specified directory '{self.working_dir}' is not a git repository: {result.stderr.strip()}"
                )
        except subprocess.SubprocessError as e:
            raise ValueError(f"Error checking git repository: {str(e)}")

    def list_models(self, substring: str = "") -> List[str]:
        """
        List available AI models that match the provided substring.

        Args:
            substring: String to match against available model names

        Returns:
            List of model name strings that match the provided substring
        """
        from aider.models import fuzzy_match_models

        # Get available models that match the substring
        return fuzzy_match_models(substring)

    def code(
        self,
        prompt: str,
        editable_files: List[str],
        readonly_files: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Run an AI coding task with the specified prompt and files.

        Args:
            prompt: Natural language instruction for the AI coding task
            editable_files: List of files that can be modified by the AI
            readonly_files: List of files that can be read but not modified

        Returns:
            Dictionary with 'success' boolean and 'diff' string showing changes
        """
        from aider.coders import Coder

        # Ensure readonly_files is a list
        if readonly_files is None:
            readonly_files = []

        # Convert relative paths to absolute paths
        abs_editable_files = [
            os.path.join(self.working_dir, file) if not os.path.isabs(file) else file
            for file in editable_files
        ]

        abs_readonly_files = [
            os.path.join(self.working_dir, file) if not os.path.isabs(file) else file
            for file in readonly_files
        ]

        # Create the coder instance
        coder = Coder.create(
            main_model=self.model,
            io=self.io,
            fnames=abs_editable_files,
            read_only_fnames=abs_readonly_files,
            auto_commits=False,
            suggest_shell_commands=False,
            detect_urls=False,
            use_git=self.use_git,
        )

        # Run the coding session
        result = coder.run(prompt)

        # Check for changes in the files and create a diff
        diff = self._get_changes_diff()

        # Check if there were meaningful changes
        success = self._check_for_meaningful_changes(editable_files)

        return {
            "success": success,
            "diff": diff,
            "result": result
        }

    def _get_changes_diff(self) -> str:
        """Get the git diff or file content if git fails."""
        import subprocess

        if not self.use_git:
            return "Git not enabled. File contents not shown."

        try:
            diff_cmd = f"git -C {self.working_dir} diff"
            diff = subprocess.check_output(
                diff_cmd, shell=True, text=True, stderr=subprocess.PIPE
            )
            return diff
        except subprocess.CalledProcessError as e:
            return f"Error getting git diff: {e.stderr.strip()}"

    def _check_for_meaningful_changes(self, relative_editable_files: List[str]) -> bool:
        """Check if the edited files contain meaningful content."""
        for file_path in relative_editable_files:
            full_path = os.path.join(self.working_dir, file_path) if not os.path.isabs(file_path) else file_path

            if os.path.exists(full_path):
                try:
                    with open(full_path, "r") as f:
                        content = f.read()
                        # Check if the file has more than just whitespace
                        stripped_content = content.strip()
                        if stripped_content and (
                            len(stripped_content.split("\n")) > 1
                            or any(
                                kw in content
                                for kw in [
                                    "def ",
                                    "class ",
                                    "import ",
                                    "from ",
                                    "async def",
                                ]
                            )
                        ):
                            return True
                except Exception:
                    continue

        return False

    def create_file(self, file_path: str, content: str) -> bool:
        """
        Create a new file with the specified content.

        Args:
            file_path: Path to the file to create (relative to working_dir)
            content: Content to write to the file

        Returns:
            True if successful, False otherwise
        """
        full_path = os.path.join(self.working_dir, file_path) if not os.path.isabs(file_path) else file_path

        try:
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w") as f:
                f.write(content)

            return True
        except Exception:
            return False

    def read_file(self, file_path: str) -> Optional[str]:
        """
        Read the content of a file.

        Args:
            file_path: Path to the file to read (relative to working_dir)

        Returns:
            Content of the file, or None if the file doesn't exist
        """
        full_path = os.path.join(self.working_dir, file_path) if not os.path.isabs(file_path) else file_path

        try:
            with open(full_path, "r") as f:
                return f.read()
        except Exception:
            return None

    def search_files(self, query: str, file_patterns: List[str] = None) -> Dict[str, List[str]]:
        """
        Search for matches in files.

        Args:
            query: String to search for
            file_patterns: List of glob patterns to limit the search to

        Returns:
            Dictionary with file paths as keys and lists of matching lines as values
        """
        import glob
        import re

        results = {}

        if file_patterns is None:
            # Default to all files
            file_patterns = ["**/*"]

        for pattern in file_patterns:
            pattern_path = os.path.join(self.working_dir, pattern)
            for file_path in glob.glob(pattern_path, recursive=True):
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r") as f:
                            content = f.read()
                            matches = re.findall(r".*" + re.escape(query) + r".*", content, re.MULTILINE)
                            if matches:
                                rel_path = os.path.relpath(file_path, self.working_dir)
                                results[rel_path] = matches
                    except Exception:
                        continue

        return results