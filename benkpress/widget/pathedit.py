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
