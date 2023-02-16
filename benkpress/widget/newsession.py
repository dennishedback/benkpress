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

from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

from benkpress.datamodel import DataframeTableModel, SampleStringStackModel
from benkpress.plugin import PluginLoader
from benkpress.ui.newsession import Ui_NewSessionDialog


class NewSessionDialog(qtw.QDialog):
    """The dialog for creating a new tagging session."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_ui()
        self._init_connections()
        self._plugin_loader = PluginLoader()

    def _init_ui(self):
        """Initialize the user interface."""
        self.ui = Ui_NewSessionDialog()
        self.ui.setupUi(self)

    def _init_connections(self):
        """Initialize connections between signals and slots."""
        ...
