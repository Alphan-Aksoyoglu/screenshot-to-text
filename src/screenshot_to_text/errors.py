from pathlib import Path
from screenshot_to_text.models.tool_type import ToolType


class S2TError(Exception):
    """Base class for s2t errors."""


class ToolNotFoundError(S2TError):
    def __init__(
        self,
        tool_type: str | None = None,
        message: str | None = None,
        looked_for_tools: list[str] | None = None,
    ):
        self.tool_type = tool_type
        self.looked_for_tools = looked_for_tools or []

        super().__init__(message or self._default_message())

    def _default_message(self) -> str:
        message = f"Cannot find a supported {self.tool_type} tool.\n"
        if self.looked_for_tools:
            message += f"Looked for {', '.join(self.looked_for_tools)}\n"
        return message


class ScreenhotToolNotFoundError(ToolNotFoundError):
    def __init__(self, message: str | None = None, looked_for_tools: list[str] | None = None):
        super().__init__(ToolType.SCREENSHOT, message, looked_for_tools)


class OCRToolNotFoundError(ToolNotFoundError):
    def __init__(self, message: str | None = None, looked_for_tools: list[str] | None = None):
        super().__init__(ToolType.OCR, message, looked_for_tools)


class ClipboardToolNotFoundError(ToolNotFoundError):
    def __init__(self, message: str | None = None, looked_for_tools: list[str] | None = None):
        super().__init__(ToolType.CLIPBOARD, message, looked_for_tools)


class ScreenshotPathNotFoundError(S2TError):
    def __init__(self, screenshot_path: Path, message: str | None = None):
        super().__init__(message)


class ConfigurationError(S2TError):
    """Base class for configuration errors."""


class ConfigOverwriteError(ConfigurationError):
    """Raised when the config file already exists and --force is not set."""

    def __init__(
        self,
        config_path: Path,
    ):
        self._default_message = f"Config file already exists at {config_path}. Please use --force to overwrite."

        super().__init__(self._default_message)


class ConfigNotFoundError(ConfigurationError):
    """Raised when the config file is not found."""

    def __init__(
        self,
        config_path: Path,
    ):
        self._default_message = f"Config file not found at {config_path}. Please run 'screenshot-to-text config' to setup the config file."

        super().__init__(self._default_message)


class InvalidConfigError(ConfigurationError):
    """Raised when the config file is not valid."""

    def __init__(
        self,
        config_path: Path,
    ):
        self._default_message = f"Config file at {config_path} is invalid."

        super().__init__(self._default_message)


class CommandError(Exception):
    """Base class for command execution errors."""


class CommandNotFoundError(CommandError):
    """Raised when the command is not found on the system."""


class CommandFailedError(CommandError):
    """Raised when a command fails."""

    def __init__(self, cmd: list[str], return_code: int, stdout: str, stderr: str):
        self.cmd = cmd
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        message = f"Command `{' '.join(cmd)}` failed with exit code {return_code}.\nStderr: {stderr}\nStdout: {stdout}"
        super().__init__(message)
