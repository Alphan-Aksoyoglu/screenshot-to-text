from enum import Enum


class ToolType(str, Enum):
    SCREENSHOT = "screenshot"
    OCR = "ocr"
    CLIPBOARD = "clipboard"
