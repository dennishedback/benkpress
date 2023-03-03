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

# TODO: Solve code duplication between read methods, specifically regarding
# cleaning of text such as " ".join(...). Perhaps using a decorator?


class Reader(Protocol):
    """A protocol for reading PDF files and returning a list of strings, one for each page."""

    def read(self, filepath: Path) -> list[str]:
        """Reads a PDF file and returns a list of strings, one for each page."""
        ...


class TesseractReader:
    """A reader that uses Tesseract OCR to read PDF files. Slow but precise."""

    def __init__(
        self,
        poppler_path: str,
        tesseract_path: str,
        tesseract_language: str,
        dpi: int = 100,
    ):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.poppler_path = poppler_path
        self.tesseract_language = tesseract_language
        self.dpi = dpi

    def read(self, filepath: Path) -> list[str]:
        images = convert_from_path(filepath, self.dpi, poppler_path=self.poppler_path)
        return [
            " ".join(
                pytesseract.image_to_string(img, lang=self.tesseract_language)
                .strip()
                .split()
            )
            for img in images
        ]

    def __repr__(self):
        return f"benkpress.api.reader.TesseractReader(tesseract_language={self.tesseract_language}, dpi={self.dpi})"


class PyPDFReader:
    """A reader that uses PyPDF2 to read PDF files. Fast but not very precise. Mostly used for testing."""

    def read(self, filepath: Path) -> list[str]:
        with filepath.open("rb") as f:
            pdf = PdfFileReader(f)
            return [
                " ".join(pdf.getPage(i).extractText().strip().split())
                for i in range(pdf.getNumPages())
            ]

    def __repr__(self):
        return "benkpress.api.reader.PyPDFReader()"
