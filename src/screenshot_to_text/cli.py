from __future__ import annotations


import typer
import click


from screenshot_to_text.config import config_file_path, default_screenshot_directory, get_tool_candidates, read_config, write_config
from screenshot_to_text.errors import ToolNotFoundError, ConfigOverwriteError, ConfigNotFoundError, InvalidConfigError

from screenshot_to_text.models.supported_platforms import Tool
from screenshot_to_text.models.s2tconfig import S2TConfig, ScreenshotConfig, OCRConfig, ClipboardConfig
from screenshot_to_text.app import capture_screenshot_and_process
from screenshot_to_text.models.tool_type import ToolType
from screenshot_to_text.constants import APP_NAME
from pydantic import ValidationError


app = typer.Typer(help=APP_NAME)


def config_choose_tool(tool_type: ToolType) -> Tool:

    tool_candidates = get_tool_candidates(tool_type)

    if not tool_candidates.available:
        raise ToolNotFoundError(tool_type.value, looked_for_tools=tool_candidates.alternative_names)

    elif len(tool_candidates.available) == 1:
        typer.echo(f" * Using {tool_candidates.available_names[0]} as {tool_type.value} tool.")
        if tool_candidates.alternative:
            typer.echo(f"\tAlternatively you can install {' or '.join(tool_candidates.alternative_names)}.")
        return tool_candidates.available[0]

    else:
        return typer.prompt(
            f"Select {tool_type.value} tool",
            type=click.Choice(tool_candidates.available_names),
        )


@app.command()
def config(
    force: bool = typer.Option(False, help="Overwrite existing config"),
    keep_screenshots: bool = typer.Option(True, help="Wether to keep screenshots"),
    keep_max_count: int = typer.Option(-1, help="Maximum number of screenshots to keep"),
    ocr_enabled: bool = typer.Option(True, help="Enable OCR"),
):

    config_path = config_file_path()

    if config_path.exists() and not force:
        raise ConfigOverwriteError(config_path)

    try:
        screenshot_tool = config_choose_tool(ToolType.SCREENSHOT)
        clipboard_tool = config_choose_tool(ToolType.CLIPBOARD)
        ocr_tool = config_choose_tool(ToolType.OCR) if ocr_enabled else Tool(name="", cmd=[])

    except ToolNotFoundError as e:
        message = (
            f"No supported {e.tool_type} tool found.\n"
            f"A {e.tool_type} tool is required, please install one of the following tools:\n"
            f"\t{', '.join(e.looked_for_tools)}\n"
            f"and try again"
        )
        typer.echo(message, err=True)
        raise typer.Exit(code=1)

    config_obj = S2TConfig(
        screenshot=ScreenshotConfig(
            tool=screenshot_tool.name,
            cmd=screenshot_tool.cmd,
            keep=keep_screenshots,
            keep_max_count=keep_max_count,
            path=default_screenshot_directory(),
        ),
        ocr=OCRConfig(
            tool=ocr_tool.name,
            enabled=ocr_enabled,
            cmd=ocr_tool.cmd,
        ),
        clipboard=ClipboardConfig(
            tool=clipboard_tool.name,
            cmd=clipboard_tool.cmd,
        ),
    )

    write_config(config_obj, config_path)

    typer.echo(f"Configuration written to {config_path}")


@app.command()
def run(
    keep_screenshot: bool | None = typer.Option(None, help="Wether to keep the screenshot, overwrites default config"),
    ocr_enabled: bool | None = typer.Option(None, help="Enable or Disable OCR, overwrites default config"),
):

    try:
        config = read_config(config_file_path())
        capture_screenshot_and_process(config, keep_screenshot, ocr_enabled)
    except ValidationError as e:
        raise InvalidConfigError(config_file_path()) from e
    except ConfigNotFoundError:
        raise


if __name__ == "__main__":
    app()
