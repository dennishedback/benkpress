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
