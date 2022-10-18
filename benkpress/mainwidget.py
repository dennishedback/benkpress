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

import urllib.parse

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtWebEngineWidgets as qtweb
from PyQt5 import QtCore as qtc

from dataset import DataframeTableModel

from pdfjswebengineview import PDFJSWebEngineView


class MainWidget(qtw.QSplitter):

    next_document_requested = qtc.pyqtSignal(bool)

    def __init__(self):
        super().__init__(qtc.Qt.Horizontal)

        self._tab_widget = qtw.QTabWidget()
        self._next_document_button = qtw.QPushButton(
            ">>> Next document >>>", clicked=self.next_document_requested
        )

        self._sidebar = qtw.QSplitter(qtc.Qt.Vertical)
        self._sidebar.addWidget(self._tab_widget)
        self._sidebar.addWidget(self._next_document_button)

        self.addWidget(self._sidebar)

    def set_document_view(self, view: qtw.QWidget) -> None:
        self.insertWidget(0, view)

    def add_page(self, page: qtw.QWidget, label: str) -> int:
        return self._tab_widget.addTab(page, label)
