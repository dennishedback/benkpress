# benkpress
# Copyright (C) 2022-2023 Dennis Hedback
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path
from typing import Protocol

import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader


class Reader(Protocol):
    """A protocol for reading PDF files and returning a list of strings, one for each page."""

    def read(self, filepath: Path) -> list[str]:
        """Reads a PDF file and returns a list of strings, one for each page."""
        ...


class TesseractReader:
    """A reader that uses Tesseract OCR to read PDF files. Slow but precise."""

    def __init__(
        self, poppler_path: str, pytesseract_path: str, lang: str, dpi: int = 100
    ):
        # FIXME: Add support to set language, dpi, paths in the GUI
        # FIXME: Error handling for incorrect paths
        pytesseract.pytesseract.tesseract_cmd = pytesseract_path
        self.poppler_path = poppler_path
        self.lang = lang
        self.dpi = dpi

    def read(self, filepath: Path) -> list[str]:
        images = convert_from_path(filepath, self.dpi, poppler_path=self.poppler_path)
        return [pytesseract.image_to_string(img, lang=self.lang) for img in images]


class PyPDFReader:
    """A reader that uses PyPDF2 to read PDF files. Fast but not very precise. Mostly used for testing."""

    def read(self, filepath: Path) -> list[str]:
        with filepath.open("rb") as f:
            pdf = PdfFileReader(f)
            return [pdf.getPage(i).extractText() for i in range(pdf.getNumPages())]
