#! /usr/bin/env python3

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

from benkpress.view.mainwindow import Ui_MainWindow


class MainWindow(qtw.QMainWindow):
    """The main window of the application."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    

class Application(qtw.QApplication):
    """The main application object."""

    def __init__(self, argv: Sequence[str]):
        super().__init__(argv)
        self._main_window = MainWindow()
        self._main_window.show()


def main():
    """The main application entrypoint."""
    app = Application(sys.argv)
    return app.exec_()


if __name__ == "__main__":
    main()
