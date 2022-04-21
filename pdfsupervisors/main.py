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

"""
phdata

Usage: pdfsupervisors <preproc> <

Options:
  --eval        Only evaluate pipeline, do not fit.
  --filewise    Feed data into pipeline on a per-file basis. Default is per-page basis. NOT IMPLEMENTED
  -o --output   Data used to fit/evaluate the pipeline. Written to stdout if not specified.
  -h --help     Show this screen.

"""

import os
import sys
from pathlib import Path
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtWebEngineWidgets as qtweb
from PyQt5 import QtCore as qtc


def get_user_data_path():
    if sys.platform.startswith("win"):
        os_path = os.getenv("LOCALAPPDATA")
    elif sys.platform.startswith("darwin"):
        os_path = "~/Library/Application Support"
    else:  # Linux
        os_path = os.getenv("XDG_DATA_HOME", "~/.local/share")
    path = Path(os_path) / "pdfsupervisors"

    if not os.path.exists(path):
        os.mkdir(path)

    return path

pdfjs = get_user_data_path() / "pdfjs" / "web" / "viewer.html"

class SupervisorWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        hbox = qtw.QHBoxLayout(self)

        # Top right split
        scroll_area_layout = qtw.QVBoxLayout()
        scroll_area = qtw.QScrollArea()
        scroll_area_widget = qtw.QWidget()
        scroll_area_widget.setLayout(scroll_area_layout)
        scroll_area.setWidget(scroll_area_widget)
        vertsplit2 = qtw.QSplitter(qtc.Qt.Vertical)
        vertsplit2.addWidget(scroll_area)
        vertsplit2.addWidget(qtw.QPushButton(">>> Next document >>>"))

        # Top split
        web_engine_view = qtweb.QWebEngineView()
        web_engine_view.load(qtc.QUrl.fromUserInput("%s?file=" % (pdfjs.as_uri())))
        horisplit = qtw.QSplitter(qtc.Qt.Horizontal)
        horisplit.addWidget(web_engine_view)
        horisplit.addWidget(vertsplit2)

        # Main Split
        table_view = qtw.QTableView()
        vertsplit1 = qtw.QSplitter(qtc.Qt.Vertical)
        vertsplit1.addWidget(horisplit)
        vertsplit1.addWidget(table_view)

        hbox.addWidget(vertsplit1)

        self.setLayout(hbox)

        #self.setDefaultGeometry(horisplit, vertsplit1, vertsplit2)
        self.setWindowTitle('PDFSupervisors')



class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setDefaultGeometry()
        self.setCentralWidget(SupervisorWidget())
        self.show()


    def setDefaultGeometry(self):  # horisplit, vertsplit1, vertsplit2):
        desktop_geometry = qtw.QDesktopWidget().availableGeometry()
        # Set window size to 60% of available width and 80% of available height
        w = desktop_geometry.right() * 0.6
        h = desktop_geometry.bottom() * 0.8
        self.resize(desktop_geometry.right() * 0.6, desktop_geometry.bottom() * 0.8)
        #horisplit.setSizes([w * 0.55, w * 0.45])
        #vertsplit1.setSizes([h * 0.7, h * 0.3])
        #vertsplit2.setSizes([h * 0.7 * 0.8, h * 0.7 * 0.2])
        qr = self.frameGeometry()
        qr.moveCenter(desktop_geometry.center())
        self.move(qr.topLeft())

def main():
    # qtw.QApplication.setStyle(qtw.QStyleFactory.create('Cleanlooks'))
    try:
        app = qtw.QApplication(sys.argv)

        if not os.path.exists(pdfjs):
            qtw.QMessageBox.critical(None, "PDF.js not found", "PDF.js not installed in user data directory. Go to "
                        "https://mozilla.github.io/pdf.js/getting_started/#download "
                        "and choose 'Stable Prebuilt (for older browsers)'. "
                        "pdfsupervisors is looking for the file %s. Extract "
                        "PDF.js accordingly." % (pdfjs))
            return 1
        win = MainWindow()
        return app.exec_()
    except Exception as e:
        qtw.QMessageBox.critical(None, "Critical error", str(e))
    finally:
        pass

if __name__ == "__main__":
    sys.exit(main())
