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


import sys
from typing import List

import PyQt6.QtWidgets as qtw

from benkpress.widget.mainwindow import MainWindow
from benkpress.widget.newsession import NewSessionDialog


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
