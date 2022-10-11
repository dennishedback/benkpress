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

"""

"""

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from benkpress.pluginloader import PluginLoader


class PreprocessorDialog(qtw.QDialog):
    set_preprocessor_requested = qtc.pyqtSignal(str)

    def __init__(self, plugin_loader: PluginLoader):
        super().__init__()
        self.setWindowTitle("Select preprocessor")
        self.resize(640, 480)
        self.setLayout(qtw.QVBoxLayout())

        available_preprocessors = plugin_loader.get_available_preprocessors()

        self._preprocessor_list_model = qtc.QStringListModel(available_preprocessors)
        self._preprocessor_list_view = qtw.QListView()
        self._preprocessor_list_view.setModel(self._preprocessor_list_model)

        if not self._preprocessor_list_model.rowCount():
            raise RuntimeError("Unable to continue: No installed preprocessors!")

        index = self._preprocessor_list_model.index(0, 0)
        self._preprocessor_list_view.setCurrentIndex(index)

        self._ok_button = qtw.QPushButton("OK")
        self._ok_button.clicked.connect(self.close)

        self.layout().addWidget(
            qtw.QLabel("Please select a preprocessor to use with this dataset:"))
        self.layout().addWidget(self._preprocessor_list_view)
        self.layout().addWidget(self._ok_button)

    def get_chosen_preprocessor(self):
        list_index = self._preprocessor_list_view.currentIndex()
        preprocessor = list_index.data(qtc.Qt.DisplayRole)
        return preprocessor
