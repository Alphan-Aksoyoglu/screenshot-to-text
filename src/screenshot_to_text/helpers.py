from __future__ import annotations

import os
import sys
import shutil
import yaml
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.abc import Traversable


def load_from_yaml(path: Traversable) -> Dict:

    with path.open("r") as f:
        data = yaml.safe_load(f)
    return data


def system_has(tool: str | None = None) -> bool:
    if not tool:
        return False
    else:
        return shutil.which(tool) is not None


def linux_session_type() -> str:
    return os.environ.get("XDG_SESSION_TYPE", "").lower()


def is_wayland() -> bool:
    return linux_session_type() == "wayland"


def get_platform() -> str:

    platform = sys.platform

    if platform == "darwin":
        platform = "macos"
    elif platform == "win32":
        platform = "windows"
    elif platform == "linux":
        platform = "linux"
        if is_wayland():
            platform += "_wayland"

    return platform
