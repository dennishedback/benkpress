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
import sys

from docopt import docopt
from PyQt5 import QtWidgets as qtw

from mainwindow import MainWindow
from settings import pdfjs


class MainApp(qtw.QApplication):
    """The main application object."""

    def __init__(self, argv):
        super().__init__(argv)
        
        args = docopt(__doc__, argv=argv[1:])
        self.main_window = MainWindow(args)
        self.main_window.show()

    def exec_(self):
        try:
            if not os.path.exists(pdfjs):
                qtw.QMessageBox.critical(None, "PDF.js not found", "PDF.js not installed in user data directory. Go to "
                            "https://mozilla.github.io/pdf.js/getting_started/#download "
                            "and choose 'Stable Prebuilt (for older browsers)'. "
                            "pdfsupervisors is looking for the file %s. Extract "
                            "PDF.js accordingly." % (pdfjs))
                return 1
            return super().exec_()
        except Exception as e:
            qtw.QMessageBox.critical(None, "Critical error", str(e))
            raise e
        finally:
            pass  # TODO: Implement workspace recovery

    @classmethod
    def main(cls):
        app = cls(sys.argv)
        app.exec_()

if __name__ == "__main__":
    sys.exit(MainApp.main())