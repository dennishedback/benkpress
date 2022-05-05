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

Usage: pdfsupervisors <pdfdir> <pipeline> <outfile>

Options:
  -o --output   Data used to fit/evaluate the pipeline. Written to stdout if not specified.
  -h --help     Show this screen.

Parameters:
  <pdfdir>      Directory containing your set of PDF files.
  <pipeline>    Joblib serialized sklearn compatible pipeline, possibly
                containing Intermediaries from the pdfsupervisors API.
  <outfile>     Output file. CSV format.

"""
#--eval        Only evaluate pipeline, do not fit.
#--filewise    Feed data into pipeline on a per-file basis. Default is per-page basis. NOT IMPLEMENTED

import os
import os.path
import sys

import PyPDF2
from sklearn.pipeline import Pipeline

from api.intermediary import Intermediary
from caller import Caller
from docopt import docopt
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

class PipelineCallbackReceiver():
    pass

class SupervisorWidget(qtw.QWidget):


    def __init__(self, files):
        super().__init__()

        self.files = files
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
        web_engine_view = qtweb.QWebEngineView()
        web_engine_view.load(qtc.QUrl.fromUserInput("%s?file=%s#pagemode=thumbs" % (pdfjs.as_uri(), self.files.pop())))
        horisplit = qtw.QSplitter(qtc.Qt.Horizontal)
        horisplit.addWidget(web_engine_view)
        horisplit.addWidget(vertsplit2)

        # Main Split
        table_view = qtw.QTableView()
        vertsplit1 = qtw.QSplitter(qtc.Qt.Vertical)
        vertsplit1.addWidget(horisplit)
        vertsplit1.addWidget(table_view)

        self.next_document_button.clicked.connect(self.on_next_document)

        hbox.addWidget(vertsplit1)

        self.setLayout(hbox)

        #self.setDefaultGeometry(horisplit, vertsplit1, vertsplit2)
        self.setWindowTitle('PDFSupervisors')
    
    @qtc.pyqtSlot()
    def on_next_document(self):
        print("hej")



class MainWindow(qtw.QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.set_default_geometry()
        files = [os.path.join(args["<pdfdir>"], f) for f in os.scandir(args["<pdfdir>"])]
        print(files[:10])
        self.setCentralWidget(SupervisorWidget(files))
        self.show()


    def set_default_geometry(self):  # horisplit, vertsplit1, vertsplit2):
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
        args = docopt(__doc__, argv=sys.argv[1:])
        app = qtw.QApplication(sys.argv)

        if not os.path.exists(pdfjs):
            qtw.QMessageBox.critical(None, "PDF.js not found", "PDF.js not installed in user data directory. Go to "
                        "https://mozilla.github.io/pdf.js/getting_started/#download "
                        "and choose 'Stable Prebuilt (for older browsers)'. "
                        "pdfsupervisors is looking for the file %s. Extract "
                        "PDF.js accordingly." % (pdfjs))
            return 1
        win = MainWindow(args)
        return app.exec_()
    except Exception as e:
        qtw.QMessageBox.critical(None, "Critical error", str(e))
    finally:
        pass

if __name__ == "__main__":
    sys.exit(main())
