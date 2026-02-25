from __future__ import annotations

from pathlib import Path
from typing import List
from pydantic import BaseModel


class ScreenshotConfig(BaseModel):
    tool: str
    cmd: List[str]
    keep: bool
    keep_max_count: int
    path: Path


class OCRConfig(BaseModel):
    tool: str | None
    enabled: bool
    cmd: List[str] | None


class ClipboardConfig(BaseModel):
    tool: str
    cmd: List[str]


class S2TConfig(BaseModel):
    screenshot: ScreenshotConfig
    ocr: OCRConfig
    clipboard: ClipboardConfig
