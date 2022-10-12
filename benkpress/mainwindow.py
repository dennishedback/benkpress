#! /usr/bin/env python3

# benkpress
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

from typing import Tuple, List

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

# from benkpress_plugins import get_available_preprocessors, get_available_pipelines
from pluginloader import PluginLoader


class MainWindow(qtw.QMainWindow):
    import_sample_requested = qtc.pyqtSignal(str)
    open_dataset_requested = qtc.pyqtSignal(str)
    new_dataset_requested = qtc.pyqtSignal()
    save_dataset_requested = qtc.pyqtSignal(str)
    change_preprocessor_requested = qtc.pyqtSignal(str)
    change_pipeline_requested = qtc.pyqtSignal(str)

    _plugin_loder: PluginLoader

    def __init__(self, plugin_loader: PluginLoader):
        super().__init__()
        self._plugin_loader = plugin_loader
        self.setWindowTitle("benkpress")
        self._setup_status_bar()
        self._setup_menu()

    def _setup_status_bar(self):
        self.statusBar().showMessage(" ", 1)  # Blank message to initiate status bar

    def _setup_menu(self):
        menu_bar = self.menuBar()  # QMenuBar

        file_menu = menu_bar.addMenu("File")  # QMenu
        file_menu.addAction("New dataset", self.new_dataset_requested)  # QAction
        file_menu.addAction("Save dataset", self.save_dataset_dialog)
        file_menu.addAction("Save dataset as", self.save_dataset_dialog)
        file_menu.addSeparator()
        file_menu.addAction("Import sample", self.import_sample_dialog)
        file_menu.addSeparator()
        file_menu.addAction("Quit", self.close)

        #################################################################
        # TODO: All code from here ...
        #################################################################

        self._build_plugin_menu(menu_bar, "Pipelines",
                                self._plugin_loader.get_available_pipelines(),
                                self.request_plugin_change)

    def _build_plugin_menu(self, menu_bar: qtw.QMenuBar, title: str,
                           plugins: List[str], action: qtc.pyqtSlot(str)):
        menu = menu_bar.addMenu(title)
        for plugin_name in plugins:
            item = menu.addAction(plugin_name, action)
            item.setCheckable(True)

    @qtc.pyqtSlot()
    def request_plugin_change(self):
        menu: qtw.QMenu = self.sender().parent()
        for action in menu.actions():
            action.setChecked(False)
        action: qtw.QAction = self.sender()
        action.setChecked(True)  # FIXME: Don't check before plugin switch confirmed

        assert menu.title() in ("Preprocessors", "Pipelines")

        if menu.title() == "Preprocessors":
            self.change_preprocessor_requested.emit(action.text())
        elif menu.title() == "Pipelines":
            self.change_pipeline_requested.emit(action.text())

    #################################################################
    # ... to here should probably be handled by a custom QMenu/QAction class
    #################################################################

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
