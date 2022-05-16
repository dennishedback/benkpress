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

import urllib.parse

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtWebEngineWidgets as qtweb
from PyQt5 import QtCore as qtc

from settings import pdfjs
from targets import PandasTableModel

class MainWidget(qtw.QWidget):
    def __init__(self, files, targets):
        super().__init__()

        self.files = files
        self.targets = targets
        hbox = qtw.QHBoxLayout(self)

        # Top right split
        scroll_area_layout = qtw.QVBoxLayout()
        scroll_area = qtw.QScrollArea()
        scroll_area_widget = qtw.QWidget()
        scroll_area_widget.setLayout(scroll_area_layout)
        scroll_area.setWidget(scroll_area_widget)
        vertsplit2 = qtw.QSplitter(qtc.Qt.Vertical)
        vertsplit2.addWidget(scroll_area)
        self.next_document_button = qtw.QPushButton(">>> Next document >>>")
        vertsplit2.addWidget(self.next_document_button)

        # Top split
        self.web_engine_view = qtweb.QWebEngineView()
        #web_engine_view.load(qtc.QUrl.fromUserInput(pdfjs))
        horisplit = qtw.QSplitter(qtc.Qt.Horizontal)
        horisplit.addWidget(self.web_engine_view)
        horisplit.addWidget(vertsplit2)

        # Main Split
        self.targets_model = PandasTableModel(self.targets)
        #table_view = TargetsView()
        table_view = qtw.QTableView()
        table_view.setModel(self.targets_model)
        #self.targets_model.dataChanged.connect(table_view.refresh)
        #self.targets_model.layoutChanged.connect(table_view.refresh)
        vertsplit1 = qtw.QSplitter(qtc.Qt.Vertical)
        vertsplit1.addWidget(horisplit)
        vertsplit1.addWidget(table_view)

        self.next_document_button.clicked.connect(self.do_next_document)

        hbox.addWidget(vertsplit1)

        self.setLayout(hbox)

        #self.setDefaultGeometry(horisplit, vertsplit1, vertsplit2)
        self.setWindowTitle('PDFSupervisors')

        self.do_next_document()

    def load_document_in_viewer(self, pdf_path):
        pdf_path_encoded = urllib.parse.quote(pdf_path)
        url = qtc.QUrl("%s?file=%s#pagemode=thumbs" % (pdfjs.as_uri(), pdf_path_encoded))
        self.targets_model.appendRow("hej.pdf", 2, "hej", 1)
        self.web_engine_view.load(url)

    
    @qtc.pyqtSlot()
    def do_next_document(self):
        #FIXME: Cannot pop from empty list
        pdf_path = self.files.pop()
        self.load_document_in_viewer(pdf_path)