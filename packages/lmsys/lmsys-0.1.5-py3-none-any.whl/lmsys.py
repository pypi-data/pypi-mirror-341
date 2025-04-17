"""
Aider SDK - Simple Python SDK for using Aider programmatically

This SDK provides an easy way to use Aider, the AI coding assistant,
in your Python scripts without dealing with the underlying complexity.
"""

import os
import json
import uuid
import tempfile
import shutil
import datetime
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
        if isinstance(self, SandboxAiderSDK):
            # If this is a SandboxAiderSDK instance, write directly to the sandbox
            full_path = os.path.join(self.working_dir, file_path) if not os.path.isabs(file_path) else file_path
            try:
                # Ensure the directory exists
                dir_path = os.path.dirname(full_path)
                if dir_path:
                    self.sandbox.commands.run(f"mkdir -p {dir_path}")

                # Write the file using both methods to ensure it works
                # Method 1: Write using the SDK
                self.sandbox.files.write(full_path, content)

                # Method 2: Also write using a command for reliability
                # Create a temporary file with the content, then use cat to write it
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                    temp.write(content)
                    temp_path = temp.name

                # Upload the temp file to the sandbox
                sandbox_temp = f"/tmp/{os.path.basename(temp_path)}"
                self.sandbox.files.write(sandbox_temp, open(temp_path, 'rb').read())

                # Use cat to write the file (more reliable for some environments)
                self.sandbox.commands.run(f"cat {sandbox_temp} > {full_path}")
                self.sandbox.commands.run(f"rm {sandbox_temp}")

                # Clean up the local temp file
                os.unlink(temp_path)

                # Verify the file exists
                if not self._file_exists_in_sandbox(full_path):
                    print(f"Warning: File {full_path} doesn't appear to exist after creation attempts.")
                    return False

                return True
            except Exception as e:
                print(f"Error creating file in sandbox: {str(e)}")
                return False
        else:
            # Original behavior for non-sandbox instance
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

    def code_headless(
        self,
        prompt: str,
        editable_files: List[str],
        readonly_files: List[str] = None,
        task_id: str = None
    ) -> Dict[str, Any]:
        """
        Run an AI coding task in headless mode without waiting for the result.

        This function starts the coding process and immediately returns a task ID
        that can be used later to check the status or retrieve results.

        Args:
            prompt: Natural language instruction for the AI coding task
            editable_files: List of files that can be modified by the AI
            readonly_files: List of files that can be read but not modified
            task_id: Optional identifier for the task (auto-generated if None)

        Returns:
            Dictionary with 'task_id' string to identify the task and 'status' string
        """
        import threading
        import uuid
        import datetime

        # Generate a task ID if not provided
        if task_id is None:
            task_id = str(uuid.uuid4())

        # Store the task status in a shared dictionary
        if not hasattr(self, '_headless_tasks'):
            self._headless_tasks = {}

        self._headless_tasks[task_id] = {
            "status": "pending",
            "result": None,
            "started_at": datetime.datetime.now().isoformat(),
        }

        # Start the coding task in a separate thread
        def run_coding_task():
            try:
                result = self.code(prompt, editable_files, readonly_files)
                self._headless_tasks[task_id] = {
                    "status": "completed",
                    "result": result,
                    "completed_at": datetime.datetime.now().isoformat(),
                }
            except Exception as e:
                self._headless_tasks[task_id] = {
                    "status": "failed",
                    "error": str(e),
                    "completed_at": datetime.datetime.now().isoformat(),
                }

        # Start the thread
        thread = threading.Thread(target=run_coding_task)
        thread.daemon = True
        thread.start()

        return {
            "task_id": task_id,
            "status": "pending"
        }

    def get_headless_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a headless coding task.

        Args:
            task_id: The ID of the task to check

        Returns:
            Dictionary with task status information
        """
        if not hasattr(self, '_headless_tasks') or task_id not in self._headless_tasks:
            return {
                "status": "not_found",
                "error": f"Task with ID {task_id} not found"
            }

        return self._headless_tasks[task_id]


class SandboxAiderSDK(AiderSDK):
    """
    Extension of AiderSDK that operates within an E2B sandbox environment.
    Allows running code, commands, and AI coding tasks in an isolated sandbox.
    """

    def __init__(
        self,
        model: str = "gemini/gemini-2.5-pro-exp-03-25",
        editor_model: Optional[str] = None,
        api_keys: Optional[Dict[str, str]] = None,
        sandbox_timeout: int = 300,  # 5 minutes default
        sandbox_id: Optional[str] = None,  # Connect to existing sandbox if provided
        user_id: Optional[str] = None,  # For tracking and persistence
    ):
        """
        Initialize the Sandbox Aider SDK.

        Args:
            model: The AI model to use for coding tasks (default: gemini-2.5-pro-exp-03-25)
            editor_model: Optional separate model for editing operations
            api_keys: Dictionary of API keys for various providers
            sandbox_timeout: Timeout in seconds for the sandbox (default: 300 seconds)
            sandbox_id: ID of existing sandbox to connect to (optional)
            user_id: User ID for tracking and persistence (optional)
        """
        # Initialize with a temporary working directory
        super().__init__(
            working_dir="/tmp",  # Temporary, will be overridden by sandbox workspace
            model=model,
            editor_model=editor_model,
            use_git=False,  # No git in sandbox by default
            api_keys=api_keys,
        )

        # Import E2B SDK
        try:
            from e2b import Sandbox
            self.Sandbox = Sandbox
        except ImportError:
            raise ImportError("E2B SDK is required. Install it with 'pip install e2b'.")

        self.user_id = user_id or str(uuid.uuid4())
        self._initialize_sandbox(sandbox_id, sandbox_timeout)

    def _initialize_sandbox(self, sandbox_id=None, timeout=300):
        """
        Initialize the E2B sandbox or connect to an existing one.

        Args:
            sandbox_id: ID of existing sandbox to connect to (optional)
            timeout: Timeout in seconds for the sandbox

        Returns:
            The initialized sandbox instance
        """
        # Use our E2B API key from environment
        if "E2B_API_KEY" not in os.environ:
            os.environ["E2B_API_KEY"] = "e2b_sk_vHhJLZxeXQvGYd7gXJOPnEYRTtnRJwJWIRm8hVeZRB6Gw6t1" # Default key, should be overridden

        # Connect to existing sandbox or create a new one
        if sandbox_id:
            self.sandbox = self.Sandbox.connect(sandbox_id)
        else:
            # Create a new sandbox with our template that has Aider pre-installed
            # Use metadata to track the user session
            self.sandbox = self.Sandbox(
                template="z7uk9vvklc16ttoijkdy",  # Template ID with Aider pre-installed
                timeout=timeout,
                metadata={
                    "user_id": self.user_id,
                    "session_start": datetime.datetime.now().isoformat()
                }
            )

        # Store sandbox info for persistence
        info = self.sandbox.get_info()
        self.sandbox_id = info.sandbox_id

        # Override working directory to point to sandbox workspace
        self.working_dir = "/home/user"  # Default workspace in E2B sandbox

        return self.sandbox

    def upload_file(self, local_path: str, sandbox_path: Optional[str] = None) -> str:
        """
        Upload a local file to the sandbox.

        Args:
            local_path: Path to local file
            sandbox_path: Path in sandbox (defaults to same filename in working_dir)

        Returns:
            Path to the file in the sandbox
        """
        if not sandbox_path:
            sandbox_path = os.path.join(self.working_dir, os.path.basename(local_path))

        with open(local_path, "rb") as f:
            content = f.read()

        self.sandbox.files.write(sandbox_path, content)
        return sandbox_path

    def write_to_sandbox(
        self,
        content: Union[str, bytes, List[Dict[str, Union[str, bytes]]], str],
        path: Optional[str] = None,
        local_directory: Optional[str] = None,
        sandbox_directory: Optional[str] = None
    ) -> List[str]:
        """
        Write file(s) to the sandbox filesystem.

        This method supports multiple ways of writing files:
        1. Single file: Provide content and path
        2. Multiple files: Provide a list of dictionaries with path and data
        3. Directory: Provide a local directory path to upload all files from that directory

        Args:
            content: File content or list of file objects with 'path' and 'data' keys,
                    or ignored if local_directory is provided
            path: Path in the sandbox for a single file upload (required if content is str/bytes)
            local_directory: Local directory path containing files to upload
            sandbox_directory: Target directory in sandbox for directory uploads (defaults to working_dir)

        Returns:
            List of paths written to the sandbox
        """
        written_paths = []

        # Create a function to ensure directory exists
        def ensure_directory_exists(dir_path):
            if dir_path:
                try:
                    self.sandbox.commands.run(f"mkdir -p {dir_path}")
                except Exception as e:
                    print(f"Warning: Could not create directory {dir_path}: {e}")

        # Case 1: Upload a directory
        if local_directory:
            if not os.path.isdir(local_directory):
                raise ValueError(f"Directory not found: {local_directory}")

            sandbox_dir = sandbox_directory or self.working_dir
            # Ensure the sandbox directory exists
            ensure_directory_exists(sandbox_dir)

            files_to_write = []

            # Iterate through all files in the directory
            for root, _, filenames in os.walk(local_directory):
                for filename in filenames:
                    local_file_path = os.path.join(root, filename)

                    # Calculate relative path from local_directory
                    rel_path = os.path.relpath(local_file_path, local_directory)
                    sandbox_file_path = os.path.join(sandbox_dir, rel_path)

                    # Ensure the directory for this file exists
                    ensure_directory_exists(os.path.dirname(sandbox_file_path))

                    # Read file contents in binary mode
                    with open(local_file_path, "rb") as file:
                        file_data = file.read()
                        files_to_write.append({
                            'path': sandbox_file_path,
                            'data': file_data
                        })
                        written_paths.append(sandbox_file_path)

            # Write all files to sandbox
            if files_to_write:
                # Try to write files individually for better reliability
                for file_obj in files_to_write:
                    try:
                        self.sandbox.files.write(file_obj['path'], file_obj['data'])

                        # Verify the file exists
                        if not self._file_exists_in_sandbox(file_obj['path']):
                            print(f"Warning: File {file_obj['path']} doesn't appear to exist after creation.")
                    except Exception as e:
                        print(f"Error writing file {file_obj['path']}: {e}")

        # Case 2: Multiple files as list of objects
        elif isinstance(content, list):
            for file_obj in content:
                if 'path' not in file_obj or 'data' not in file_obj:
                    raise ValueError("Each file object must contain 'path' and 'data' keys")

                # Ensure the directory for this file exists
                ensure_directory_exists(os.path.dirname(file_obj['path']))

                try:
                    self.sandbox.files.write(file_obj['path'], file_obj['data'])
                    written_paths.append(file_obj['path'])

                    # Verify the file exists
                    if not self._file_exists_in_sandbox(file_obj['path']):
                        print(f"Warning: File {file_obj['path']} doesn't appear to exist after creation.")
                except Exception as e:
                    print(f"Error writing file {file_obj['path']}: {e}")

        # Case 3: Single file
        elif path:
            # Ensure the directory for this file exists
            ensure_directory_exists(os.path.dirname(path))

            try:
                self.sandbox.files.write(path, content)
                written_paths.append(path)

                # Verify the file exists
                if not self._file_exists_in_sandbox(path):
                    print(f"Warning: File {path} doesn't appear to exist after creation.")
            except Exception as e:
                print(f"Error writing file {path}: {e}")

        else:
            raise ValueError("Either path (for single file) or a list of file objects or local_directory must be provided")

        return written_paths

    def download_file(self, sandbox_path: str, local_path: Optional[str] = None) -> str:
        """
        Download a file from the sandbox to local filesystem.

        Args:
            sandbox_path: Path to file in sandbox
            local_path: Path to download to (defaults to same filename)

        Returns:
            Path to the downloaded file
        """
        if not local_path:
            local_path = os.path.basename(sandbox_path)

        content = self.sandbox.files.read(sandbox_path)

        # Handle both string and bytes content types
        if isinstance(content, str):
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            with open(local_path, "wb") as f:
                f.write(content)

        return local_path

    def read_sandbox_file(self, sandbox_path: str, as_string: bool = True, encoding: str = "utf-8") -> Union[str, bytes]:
        """
        Read a file from the sandbox.

        Args:
            sandbox_path: Path to the file in the sandbox
            as_string: Whether to return the content as a string (True) or bytes (False)
            encoding: Encoding to use when converting bytes to string (default: utf-8)

        Returns:
            File content as string or bytes depending on as_string parameter
        """
        try:
            content = self.sandbox.files.read(sandbox_path)

            # If content is bytes and as_string is True, decode to string
            if isinstance(content, bytes) and as_string:
                return content.decode(encoding)
            # If content is string and as_string is False, encode to bytes
            elif isinstance(content, str) and not as_string:
                return content.encode(encoding)
            # Otherwise return as is
            else:
                return content
        except Exception as e:
            raise ValueError(f"Error reading file '{sandbox_path}': {str(e)}")

    def run_command(self, command: str) -> Dict[str, Any]:
        """
        Run a command in the sandbox.

        Args:
            command: Command to run

        Returns:
            Dictionary with command result info
        """
        result = self.sandbox.commands.run(command)

        return {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def _file_exists_in_sandbox(self, file_path: str) -> bool:
        """
        Check if a file exists in the sandbox.

        Args:
            file_path: Path to file in sandbox

        Returns:
            True if file exists, False otherwise
        """
        try:
            # More reliable approach: try to list the directory and check if the file exists
            # Extract the directory and filename
            import os
            directory = os.path.dirname(file_path) or "/"
            filename = os.path.basename(file_path)

            # Run a command to check if the file exists (more reliable than stat)
            result = self.sandbox.commands.run(f"ls -la {directory} | grep {filename}")
            return result.exit_code == 0 and filename in result.stdout
        except Exception as e:
            print(f"Error checking if file exists: {str(e)}")
            # Fallback to the original approach
            try:
                self.sandbox.files.stat(file_path)
                return True
            except Exception:
                return False

    def sandbox_code(
        self,
        prompt: str,
        editable_files: List[str],
        readonly_files: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Run an AI coding task in the sandbox with the specified prompt and files.

        Args:
            prompt: Natural language instruction for the AI coding task
            editable_files: List of files in the sandbox that can be modified by the AI
            readonly_files: List of files in the sandbox that can be read but not modified

        Returns:
            Dictionary with 'success' boolean and 'diff' string showing changes
        """
        if readonly_files is None:
            readonly_files = []

        # First verify all files exist in the sandbox using commands
        missing_files = []
        all_files = editable_files + readonly_files

        # Use a more direct command to check all files at once
        if all_files:
            file_list_str = " ".join(all_files)
            result = self.sandbox.commands.run(f"ls -la {file_list_str} 2>&1 || echo 'FILES_MISSING'")

            if "FILES_MISSING" in result.stdout or "No such file or directory" in result.stdout:
                # Some files might be missing, check each one individually
                for path in all_files:
                    # Get absolute path if not already
                    abs_path = path if os.path.isabs(path) else os.path.join(self.working_dir, path)
                    # Check file existence with a direct command
                    check_result = self.sandbox.commands.run(f"[ -f '{abs_path}' ] && echo 'EXISTS' || echo 'MISSING'")

                    if "MISSING" in check_result.stdout:
                        missing_files.append(path)
                        print(f"Warning: File '{path}' does not appear to exist in the sandbox")

        # If files are missing, try to create them with empty content as a fallback
        if missing_files:
            print(f"Attempting to create missing files: {missing_files}")
            for path in missing_files:
                try:
                    # Create empty file
                    abs_path = path if os.path.isabs(path) else os.path.join(self.working_dir, path)
                    dir_path = os.path.dirname(abs_path)
                    if dir_path:
                        self.sandbox.commands.run(f"mkdir -p '{dir_path}'")
                    self.sandbox.commands.run(f"touch '{abs_path}'")

                    # Verify it was created
                    check_result = self.sandbox.commands.run(f"[ -f '{abs_path}' ] && echo 'EXISTS' || echo 'MISSING'")
                    if "MISSING" in check_result.stdout:
                        raise ValueError(f"Failed to create missing file: {path}")
                except Exception as e:
                    raise ValueError(f"Error creating missing file '{path}': {str(e)}")

        # Run the coding task with sandbox paths
        result = self._run_sandbox_coding_task(prompt, editable_files, readonly_files)

        return result

    def _run_sandbox_coding_task(self, prompt, editable_files, readonly_files):
        """
        Helper to run coding tasks in sandbox context.

        Args:
            prompt: Natural language instruction for the AI coding task
            editable_files: List of files in the sandbox that can be modified by the AI
            readonly_files: List of files in the sandbox that can be read but not modified

        Returns:
            Dictionary with task result information
        """
        # Download files from sandbox to temporary local directory
        temp_dir = tempfile.mkdtemp()
        local_editable_files = []
        local_readonly_files = []

        try:
            # Download editable files
            for file in editable_files:
                local_path = os.path.join(temp_dir, os.path.basename(file))
                content = self.sandbox.files.read(file)
                if isinstance(content, str):
                    content = content.encode()
                with open(local_path, "wb") as f:
                    f.write(content)
                local_editable_files.append(local_path)

            # Download readonly files
            for file in readonly_files:
                local_path = os.path.join(temp_dir, os.path.basename(file))
                content = self.sandbox.files.read(file)
                if isinstance(content, str):
                    content = content.encode()
                with open(local_path, "wb") as f:
                    f.write(content)
                local_readonly_files.append(local_path)

            # Temporarily override working directory for local operation
            original_working_dir = self.working_dir
            self.working_dir = temp_dir

            # Perform coding task locally
            try:
                result = self.code(prompt, [os.path.basename(f) for f in local_editable_files],
                                 [os.path.basename(f) for f in local_readonly_files])
            finally:
                # Restore working directory
                self.working_dir = original_working_dir

            # Upload modified files back to sandbox
            for local_file, sandbox_file in zip([os.path.join(temp_dir, os.path.basename(f)) for f in editable_files],
                                              editable_files):
                if os.path.exists(local_file):
                    with open(local_file, "rb") as f:
                        content = f.read()
                    self.sandbox.files.write(sandbox_file, content)

            return result

        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir)

    def extend_sandbox_timeout(self, seconds: int = 300) -> None:
        """
        Extend the sandbox timeout.

        Args:
            seconds: Number of seconds to extend the timeout by
        """
        self.sandbox.set_timeout(seconds)

    def get_sandbox_info(self) -> Dict[str, Any]:
        """
        Get information about the current sandbox.

        Returns:
            Dictionary with sandbox information
        """
        info = self.sandbox.get_info()
        return {
            "sandbox_id": info.sandbox_id,
            "template_id": info.template_id,
            "started_at": info.started_at,
            "end_at": info.end_at,
            "metadata": info.metadata,
        }

    def kill_sandbox(self) -> Dict[str, Any]:
        """
        Shutdown the sandbox immediately.

        This will terminate the sandbox regardless of its remaining timeout.
        Once killed, the sandbox cannot be restarted.

        Returns:
            Dictionary with kill status information
        """
        try:
            self.sandbox.kill()
            return {
                "success": True,
                "sandbox_id": self.sandbox_id,
                "message": f"Sandbox {self.sandbox_id} has been successfully terminated."
            }
        except Exception as e:
            return {
                "success": False,
                "sandbox_id": self.sandbox_id,
                "error": str(e),
                "message": f"Failed to terminate sandbox {self.sandbox_id}."
            }