#! /usr/bin/env python3

# pdfsupervisors
# Copyright (C) 2022 Dennis Hedback
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

import os

import pandas as pd

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from mainwidget import MainWidget

class MainWindow(qtw.QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.set_default_geometry()
        self.setup_status_bar()
        self.setup_menu()
        # FIXME: Gracefully handle incorrect file paths
        files = [os.path.join(args["<pdfdir>"], f) for f in os.scandir(args["<pdfdir>"])]
        #print(files[:10])
        targets = pd.DataFrame({"target": ["foo"], "class": [0]})
        self.setCentralWidget(MainWidget(files, targets))

    def setup_status_bar(self):
        self.statusBar().showMessage(" ", 1)  # Blank message to initiate status bar

    def setup_menu(self):
        menu_bar = self.menuBar()  # QMenuBar
        file_menu = menu_bar.addMenu("File")  # QMenu
        file_menu.addAction("New dataset")
        file_menu.addAction("Open dataset", self.open_dataset)
        file_menu.addAction("Save dataset")  # QAction
        file_menu.addAction("Save dataset as")
        file_menu.addSeparator()
        file_menu.addAction("Import sample")
        file_menu.addAction("Import pipeline")
        file_menu.addSeparator()
        file_menu.addAction("Quit", self.close)

    @qtc.pyqtSlot()
    def open_dataset(self):
        filename, _ = qtw.QFileDialog.getOpenFileName()
        if filename:
            self.statusBar().showMessage(filename)


    def set_default_geometry(self):  # horisplit, vertsplit1, vertsplit2):
        desktop_geometry = qtw.QDesktopWidget().availableGeometry()
        # Set window size to 60% of available width and 80% of available height
        w = desktop_geometry.right() * 0.6
        h = desktop_geometry.bottom() * 0.8
        self.resize(int(desktop_geometry.right() * 0.6), int(desktop_geometry.bottom() * 0.8))
        #horisplit.setSizes([w * 0.55, w * 0.45])
        #vertsplit1.setSizes([h * 0.7, h * 0.3])
        #vertsplit2.setSizes([h * 0.7 * 0.8, h * 0.7 * 0.2])
        qr = self.frameGeometry()
        qr.moveCenter(desktop_geometry.center())
        self.move(qr.topLeft())