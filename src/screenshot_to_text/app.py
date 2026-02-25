import subprocess
from screenshot_to_text.models.s2tconfig import S2TConfig, ScreenshotConfig, OCRConfig, ClipboardConfig
from datetime import datetime
from pathlib import Path
import collections
from screenshot_to_text.errors import CommandNotFoundError, CommandFailedError, ToolNotFoundError
from platformdirs import user_cache_dir
from screenshot_to_text.helpers import system_has

from screenshot_to_text.constants import APP_NAME
from pypdf import PdfReader
import cv2
import numpy as np


def run_command(cmd: list[str], text_input: str | None = None, capture: bool = True) -> str:
    stdout = subprocess.PIPE if capture else subprocess.DEVNULL
    stderr = subprocess.PIPE if capture else subprocess.DEVNULL

    if not cmd:
        raise CommandNotFoundError("Command not found, cmd is None")
    if not system_has(cmd[0]):
        raise CommandNotFoundError(f"Command not found: {cmd[0]}")

    try:
        process = subprocess.run(
            cmd,
            input=text_input,
            check=True,
            text=True,
            stdout=stdout,
            stderr=stderr,
        )
        return process.stdout or ""
    except FileNotFoundError as e:
        raise CommandNotFoundError(f"Command not found: {cmd[0]}") from e
    except subprocess.CalledProcessError as e:
        stdout = e.stdout or ""
        stderr = e.stderr or ""
        raise CommandFailedError(
            cmd=cmd,
            return_code=e.returncode,
            stdout=stdout,
            stderr=stderr,
        ) from e


def validate_tool(config: ScreenshotConfig | OCRConfig | ClipboardConfig):
    if not config.tool or not system_has(config.tool):
        raise ToolNotFoundError(config.tool)


def validate_command(config: ScreenshotConfig | OCRConfig | ClipboardConfig):
    if not config.cmd or not system_has(config.cmd[0]):
        raise CommandNotFoundError


def runtime_validate(config: ScreenshotConfig | OCRConfig | ClipboardConfig):
    validate_tool(config)
    validate_command(config)


def take_screenshot(screenshot_config: ScreenshotConfig, screenshot_dir: Path) -> Path:

    runtime_validate(screenshot_config)

    filename = screenshot_dir / f"screenshot_{datetime.now().isoformat().replace(':', '_')}.png"

    run_command(screenshot_config.cmd + [str(filename)], capture=False)

    return filename


def run_ocr(ocr_config: OCRConfig, filename: Path) -> Path | None:

    runtime_validate(ocr_config)

    if ocr_config.cmd:
        filename_png = str(filename)
        filename_pdf = str(filename).replace(".png", "")

        cmd = [arg.format(filename=filename_png, filename_pdf=filename_pdf) for arg in ocr_config.cmd]
        run_command(cmd)
        return Path(filename_pdf + ".pdf")


def pdf_to_txt_with_layout(path: Path) -> str:
    reader = PdfReader(path)
    page = reader.pages[0]
    text = page.extract_text(extraction_mode="layout")
    return text


def preprocess_screenshot_for_ocr(filename: Path):

    image = cv2.imread(filename)

    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img_resized = cv2.resize(grayscale_image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    # Thresholding to remove noise and make text solid black
    _, thresh = cv2.threshold(img_resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Dilation to make underscores more visible
    kernel = np.ones((2, 2), np.uint8)
    processed_image = cv2.dilate(thresh, kernel, iterations=1)

    processed_filename = filename.parent / (filename.name.replace(".png", "") + "_processed.png")

    cv2.imwrite(processed_filename, processed_image)

    return processed_filename


def copy_text_to_clipboard(clipboard_config: ClipboardConfig, text: str):
    runtime_validate(clipboard_config)
    run_command(clipboard_config.cmd, text_input=text, capture=False)


def cleanup_screenshots(path: Path, keep_max_count: int):
    if keep_max_count == -1:
        return

    files_by_basename = collections.defaultdict(list)

    # Group all relevant files by their base name
    for p in path.glob("*.png"):
        if p.name.endswith("_processed.png"):
            base_name = p.stem.removesuffix("_processed")
        else:
            base_name = p.stem
        files_by_basename[base_name].append(p)

    for p in path.glob("*.pdf"):
        base_name = p.stem
        files_by_basename[base_name].append(p)

    screenshot_groups = []
    for base_name, files in files_by_basename.items():
        try:
            latest_ctime = max(p.stat().st_ctime for p in files)
            screenshot_groups.append((latest_ctime, files))
        except FileNotFoundError:
            continue

    screenshot_groups.sort(key=lambda x: x[0], reverse=True)

    groups_to_delete = screenshot_groups[keep_max_count:]

    for _, files in groups_to_delete:
        for file_path in files:
            file_path.unlink(missing_ok=True)


def capture_screenshot_and_process(config: S2TConfig, keep_screenshot: bool | None = None, ocr_enabled: bool | None = None):

    is_ocr_enabled = ocr_enabled if ocr_enabled is not None else config.ocr.enabled
    is_screenshot_kept = keep_screenshot if keep_screenshot is not None else config.screenshot.keep

    if is_screenshot_kept:
        screenshot_dir = Path(config.screenshot.path)
        if not screenshot_dir.exists():
            screenshot_dir.mkdir(parents=True, exist_ok=True)
    else:
        screenshot_dir = Path(user_cache_dir(APP_NAME))
        if not screenshot_dir.exists():
            screenshot_dir.mkdir(parents=True, exist_ok=True)

    filename = take_screenshot(config.screenshot, screenshot_dir)

    if is_ocr_enabled:
        preprocessed_file = preprocess_screenshot_for_ocr(filename)
        text = pdf_to_txt_with_layout(run_ocr(config.ocr, preprocessed_file))

        if text:
            copy_text_to_clipboard(config.clipboard, text)

    if is_screenshot_kept and config.screenshot.keep_max_count > 0:
        cleanup_screenshots(screenshot_dir, config.screenshot.keep_max_count)
