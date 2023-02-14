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


class Application(qtw.QApplication):
    """The main application object."""

    main_window: MainWindow

    def __init__(self, argv: List[str]):
        super().__init__(argv)
        self._init_ui()
        self._connect_signals()
        self.main_window.ui.web_engine_view.load(r"C:\Users\denhed\Downloads\Dennis Hedback.pdf")

    def _init_ui(self):
        """Initialize the user interface."""
        self.main_window = MainWindow()
        self.main_window.show()

    def _connect_signals(self):
        """Connect signals to slots."""
        self.main_window.ui.next_document.clicked.connect(lambda: print("Next document!"))




def main():
    """The main application entrypoint."""
    app = Application(sys.argv)
    return app.exec()


if __name__ == "__main__":
    main()
