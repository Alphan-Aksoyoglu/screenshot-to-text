import pytest
from screenshot_to_text.app import take_screenshot
from screenshot_to_text.models.s2tconfig import ScreenshotConfig
from screenshot_to_text.errors import ToolNotFoundError
from screenshot_to_text.app import run_ocr, capture_screenshot_and_process
from screenshot_to_text.models.s2tconfig import OCRConfig, S2TConfig, ClipboardConfig
from screenshot_to_text.errors import CommandError


@pytest.mark.parametrize("tool", ["", " "])
def test_take_screenshot_no_tool(mocker, tmp_path, tool):
    """
    None handled by pydantic
    """
    config = ScreenshotConfig(
        tool=tool,
        cmd=[],
        keep=True,
        keep_max_count=-1,
        path=tmp_path._str,
    )

    with pytest.raises(ToolNotFoundError):
        take_screenshot(config, tmp_path)


@pytest.mark.parametrize("tool", [None, "", " "])
def test_ocr_no_tool(tmp_path, tool):

    config = OCRConfig(tool=tool, enabled=True, cmd=[])

    with pytest.raises(ToolNotFoundError):
        run_ocr(config, tmp_path)


@pytest.mark.parametrize("cmd", [None, [], [""], [" "]])
def test_ocr_no_command(mocker, tmp_path, cmd):
    """
    [None] handled by pydantic
    """
    config = OCRConfig(
        tool="some tool",
        enabled=True,
        cmd=cmd,
    )

    mocker.patch("screenshot_to_text.app.validate_tool")

    with pytest.raises(CommandError):
        run_ocr(config, tmp_path)


@pytest.mark.parametrize("tool", ["", " "])
def test_ocr_enabled_clipboard_no_tool(mocker, tmp_path, tool):

    config = S2TConfig(
        screenshot=ScreenshotConfig(
            tool="some tool",
            cmd=[],
            keep=True,
            keep_max_count=-1,
            path=tmp_path._str,
        ),
        ocr=OCRConfig(
            tool="some tool",
            enabled=True,
            cmd=[],
        ),
        clipboard=ClipboardConfig(
            tool=tool,
            cmd=[],
        ),
    )

    mocker.patch("screenshot_to_text.app.run_ocr", return_value=tmp_path / "some.pdf")
    mocker.patch("screenshot_to_text.app.take_screenshot", return_value=tmp_path / "some.png")
    mocker.patch("screenshot_to_text.app.preprocess_screenshot_for_ocr", return_value=tmp_path / "some_processed.png")
    mocker.patch("screenshot_to_text.app.pdf_to_txt_with_layout", return_value="some text")

    with pytest.raises(ToolNotFoundError):
        capture_screenshot_and_process(config)


@pytest.mark.parametrize("cmd", [[], [""], [" "]])
def test_ocr_enabled_clipboard_no_command(mocker, tmp_path, cmd):
    """
    [None] handled by pydantic
    """
    config = S2TConfig(
        screenshot=ScreenshotConfig(
            tool="some tool",
            cmd=[],
            keep=True,
            keep_max_count=-1,
            path=tmp_path._str,
        ),
        ocr=OCRConfig(
            tool="some tool",
            enabled=True,
            cmd=[],
        ),
        clipboard=ClipboardConfig(
            tool="some tool",
            cmd=cmd,
        ),
    )

    mocker.patch("screenshot_to_text.app.run_ocr", return_value=tmp_path / "some.pdf")
    mocker.patch("screenshot_to_text.app.take_screenshot", return_value=tmp_path / "some.png")
    mocker.patch("screenshot_to_text.app.preprocess_screenshot_for_ocr", return_value=tmp_path / "some_processed.png")
    mocker.patch("screenshot_to_text.app.pdf_to_txt_with_layout", return_value="some text")
    mocker.patch("screenshot_to_text.app.validate_tool")

    with pytest.raises(CommandError):
        capture_screenshot_and_process(config)
