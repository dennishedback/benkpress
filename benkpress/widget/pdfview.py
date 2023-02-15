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

import os.path
import urllib.parse
from pathlib import Path

import PyQt6.QtCore as qtc
import PyQt6.QtWebEngineWidgets as qtweb
from appdirs import user_data_dir

# TODO: Decide where this setting should be stored

pdfjs = (
    Path(user_data_dir("benkpress", "dennishedback")) / "pdfjs" / "web" / "viewer.html"
)

# FIXME: Should be able to do this using only pathlib

if not os.path.exists(pdfjs):
    raise Exception(
        "PDF.js not found",
        "PDF.js not installed in user data directory. Go to "
        "https://mozilla.github.io/pdf.js/getting_started/#download "
        "and choose 'Stable Prebuilt (for older browsers)'. "
        "benkpress is looking for the file %s. Extract "
        "PDF.js accordingly." % (pdfjs),
    )


class PDFView(qtweb.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def load(self, filepath: str) -> None:
        filepath_encoded = urllib.parse.quote(filepath)
        url = qtc.QUrl(
            "%s?file=%s#pagemode=thumbs" % (pdfjs.as_uri(), filepath_encoded)
        )
        super().load(url)
