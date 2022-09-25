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

from typing import Tuple
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):

    import_sample_requested = qtc.pyqtSignal(str)
    open_dataset_requested = qtc.pyqtSignal(str)
    new_dataset_requested = qtc.pyqtSignal()
    save_dataset_requested = qtc.pyqtSignal(str)
    import_context_requested = qtc.pyqtSignal(str)
    import_pipeline_requested = qtc.pyqtSignal(str)
    import_preproc_requested = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFSupervisors")
        self._setup_status_bar()
        self._setup_menu()

    def _setup_status_bar(self):
        self.statusBar().showMessage(" ", 1)  # Blank message to initiate status bar

    def _setup_menu(self):
        menu_bar = self.menuBar()  # QMenuBar
        file_menu = menu_bar.addMenu("File")  # QMenu
        file_menu.addAction("New dataset", self.new_dataset_requested)  # QAction
        file_menu.addAction("Open dataset", self.open_dataset_dialog)
        file_menu.addAction("Save dataset", self.save_dataset_dialog)
        file_menu.addAction("Save dataset as", self.save_dataset_dialog)
        file_menu.addSeparator()
        file_menu.addAction("Import context", self.import_context_dialog)
        #file_menu.addAction("Import pipeline", self.import_pipeline_dialog)
        #file_menu.addAction("Import preprocessor", self.import_preproc_dialog)
        file_menu.addAction("Import sample", self.import_sample_dialog)
        file_menu.addSeparator()
        file_menu.addAction("Quit", self.close)

    @qtc.pyqtSlot()
    def open_dataset_dialog(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            caption="Open dataset",
            filter="All files (*.*);;Comma separated values (*.csv)",
            initialFilter="Comma separated values (*.csv)",
        )
        if filename:
            self.open_dataset_requested.emit(filename)

    @qtc.pyqtSlot()
    def save_dataset_dialog(self):
        filename, _ = qtw.QFileDialog.getSaveFileName(
            caption="Save dataset",
            filter="All files (*.*);;Comma separated values (*.csv)",
            initialFilter="Comma separated values (*.csv)",
        )
        if filename:
            self.save_dataset_requested.emit(filename)

    @qtc.pyqtSlot()
    def import_sample_dialog(self):
        directory = qtw.QFileDialog.getExistingDirectory(caption="Import sample")
        if directory:
            self.import_sample_requested.emit(directory)

    @qtc.pyqtSlot()
    def import_context_dialog(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            caption="Import context",
            filter="All files (*.*);;Serialized PDFClassifierContext (*.joblib)",
            initialFilter="Serialized PDFClassifierContext (*.joblib)",
        )
        if filename:
            self.import_context_requested.emit(filename)

    @qtc.pyqtSlot()
    def import_pipeline_dialog(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            caption="Import pipeline",
            filter="All files (*.*);;Serialized pipeline (*.joblib)",
            initialFilter="Serialized pipeline (*.joblib)",
        )
        if filename:
            self.import_pipeline_requested.emit(filename)

    @qtc.pyqtSlot()
    def import_preproc_dialog(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            caption="Import preprocessor",
            filter="All files (*.*);;Serialized preprocessor (*.joblib)",
            initialFilter="Serialized preprocessor (*.joblib)",
        )
        if filename:
            self.import_preproc_requested.emit(filename)

    def set_default_geometry(self) -> Tuple[int, int]:
        desktop_geometry = qtw.QDesktopWidget().availableGeometry()
        # Set window size to 60% of available width and 80% of available height
        w = int(desktop_geometry.right() * 0.6)
        h = int(desktop_geometry.bottom() * 0.8)
        self.resize(w, h)
        qr = self.frameGeometry()
        qr.moveCenter(desktop_geometry.center())
        self.move(qr.topLeft())
        return (w, h)
