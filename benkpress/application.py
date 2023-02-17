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

"""Module containing the application class as well as top-level windows and dialogs."""

import sys
from typing import List

import PyQt6.QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

from benkpress.datamodel import DataframeTableModel, SampleStringStackModel
from benkpress.plugin import PluginLoader
from benkpress.ui.mainwindow import Ui_MainWindow
from benkpress.ui.newsession import Ui_NewSessionDialog


class MainWindow(qtw.QMainWindow):
    """The main window of the application."""

    new_session_requested = qtc.pyqtSignal()
    quit_requested = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_ui()
        self._init_connections()
        self._init_models()

    def _init_ui(self):
        """Initialize the user interface."""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def _init_connections(self):
        """Initialize connections between signals and slots."""
        # TODO: Should consider dataset save state before most of these actions.
        self.ui.action_new_session.triggered.connect(self.request_new_session)
        self.ui.action_exit.triggered.connect(self.quit_requested.emit)

        ...

    def _init_models(self):
        """Initialize the application models."""
        self.sample = SampleStringStackModel()
        self.dataset = DataframeTableModel()

    @qtc.pyqtSlot()
    def request_new_session(self):
        # TODO: Should consider dataset save state before this action.§
        self.new_session_requested.emit()

    @qtc.pyqtSlot()
    def show_save_dataset_dialog(self):
        filename, _ = qtw.QFileDialog.getSaveFileName(
            caption="Save dataset",
            filter="All files (*.*);;Comma separated values (*.csv)",
            initialFilter="Comma separated values (*.csv)",
        )
        if filename:
            ...
            # self.save_dataset_requested.emit(filename)

    @qtc.pyqtSlot()
    def show_import_sample_dialog(self):
        directory = qtw.QFileDialog.getExistingDirectory(caption="Import sample")
        if directory:
            ...
            # self.import_sample_requested.emit(directory)


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


class Application(qtw.QApplication):
    """The main application object."""

    main_window: MainWindow
    new_session_dialog: NewSessionDialog

    def __init__(self, argv: List[str]):
        super().__init__(argv)
        self._init_windows()
        self._init_connections()

    def _init_windows(self):
        """Initialize the application windows and dialogs."""
        self.main_window = MainWindow()
        self.main_window.show()
        self.new_session_dialog = NewSessionDialog(parent=self.main_window)

    def _init_connections(self):
        """Initialize connections between signals and slots."""
        self.main_window.new_session_requested.connect(self._open_new_session_dialog)
        self.main_window.quit_requested.connect(self.quit)

    def _open_new_session_dialog(self):
        """Open the new session dialog."""
        hej = self.new_session_dialog.open()
        print(hej)


def main():
    """The main application entrypoint."""
    return Application(sys.argv).exec()


if __name__ == "__main__":
    sys.exit(main())
