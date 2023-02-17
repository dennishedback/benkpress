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

"""Module containing custom widgets that is not top-level windows or dialogs."""


import os.path
import urllib.parse
from pathlib import Path

import PyQt6.QtCore as qtc
import PyQt6.QtWebEngineWidgets as qtweb
from appdirs import user_data_dir
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from spacy.util import get_installed_models

from benkpress.plugin import PluginLoader


class PageFilterBox(qtw.QComboBox):
    """A combobox for selecting a page filter plugin."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._plugin_loader = PluginLoader()
        self.addItems(self._plugin_loader.get_available_page_filters())


class PipelineBox(qtw.QComboBox):
    """A combobox for selecting a pipeline plugin."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._plugin_loader = PluginLoader()
        self.addItems(self._plugin_loader.get_available_pipelines())


class SpacyModelsBox(qtw.QComboBox):
    """A combobox for selecting a tokenizer plugin."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(get_installed_models())


class ReaderBox(qtw.QComboBox):
    """ "A combobox for selecting PDF reader."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(["Tesseract", "PyPDF"])


class PathEdit(qtw.QLineEdit):
    """A path edit widget that allows the user to select a path using a file dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_actions()

    def _init_actions(self):
        """Initialize actions."""
        action = qtg.QAction(
            self.style().standardIcon(qtw.QStyle.StandardPixmap.SP_DirIcon), "", self
        )
        self.addAction(action, qtw.QLineEdit.ActionPosition.TrailingPosition)
        action.triggered.connect(self._open_dialog)

    def _open_dialog(self):
        """Open the file dialog."""
        if self.property("folder"):
            path = qtw.QFileDialog.getExistingDirectory(self, "Select directory")
        else:
            path = qtw.QFileDialog.getOpenFileName(self, "Select file")[0]
        if path:
            self.setText(path)


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
