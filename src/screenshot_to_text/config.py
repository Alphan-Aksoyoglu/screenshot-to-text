from __future__ import annotations

import tomllib
from pathlib import Path
import tomli_w
from platformdirs import user_config_dir, user_pictures_path
from importlib import resources
import screenshot_to_text.data as data
from screenshot_to_text.models.supported_platforms import SupportedPlatforms, Tool
from screenshot_to_text.models.s2tconfig import S2TConfig
from screenshot_to_text.models.tool_type import ToolType
from dataclasses import dataclass
from screenshot_to_text.helpers import get_platform, system_has, load_from_yaml
from screenshot_to_text.errors import ConfigNotFoundError
from screenshot_to_text.constants import APP_NAME

yaml_config_path = resources.files(data)
yaml_resources = resources.files(data)

supported_platforms_yaml = yaml_resources / "supported_platforms.yaml"
supported_platforms_dict = load_from_yaml(supported_platforms_yaml)

supported_platforms = SupportedPlatforms.model_validate(supported_platforms_dict)


@dataclass
class ToolCandidates:
    available: list[Tool]
    alternative: list[Tool]
    available_names: list[str]
    alternative_names: list[str]


def config_dir() -> Path:
    return Path(user_config_dir(APP_NAME))


def config_file_path() -> Path:
    return config_dir() / "config.toml"


def default_screenshot_directory() -> Path:
    return user_pictures_path() / APP_NAME / "screenshots"


def read_config(config_path: Path) -> S2TConfig:
    if not config_path.exists():
        raise ConfigNotFoundError(config_path)

    with open(config_path, "rb") as f:
        config_data = tomllib.load(f)
    return S2TConfig.model_validate(config_data)


def write_config(config: S2TConfig, config_path: Path) -> None:
    config_dir = config_path.parent
    config_dir.mkdir(parents=True, exist_ok=True)

    config_data = config.model_dump(mode="json")

    with open(config_path, "wb") as f:
        tomli_w.dump(config_data, f)


def get_tool_candidates(tool_type: ToolType, platform: str | None = None) -> ToolCandidates:

    if not platform:
        platform = get_platform()

    tool_candidates = ToolCandidates(
        available=supported_platforms.get(platform).get(tool_type).available_tools(system_has),
        alternative=supported_platforms.get(platform).get(tool_type).alternative_tools(system_has),
        available_names=[],
        alternative_names=[],
    )

    tool_candidates.available_names = [tool.name for tool in tool_candidates.available]
    tool_candidates.alternative_names = [tool.name for tool in tool_candidates.alternative]

    return tool_candidates
