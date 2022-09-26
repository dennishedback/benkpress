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


import random
import os
import sys

import joblib
import pandas as pd
import PyPDF2

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from sklearn.exceptions import NotFittedError
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.model_selection import train_test_split

from mainwidget import MainWidget
from mainwindow import MainWindow
from model import DataframeTableModel, SampleStringStackModel
from pdfjswebengineview import PDFJSWebEngineView

RANDOM_STATE = 999


class MainApp(qtw.QApplication):
    """The main application object."""

    def __init__(self, argv):
        super().__init__(argv)

        self._context = None
        #self._preprocessor = None  # AuditReportPageFirstSentenceTargetPreprocessor()
        #self._pipe = None

        self._pdf_view = PDFJSWebEngineView()
        self._dataset_model = DataframeTableModel()
        self._sample_model = SampleStringStackModel()

        self._dataset_view = qtw.QTableView()
        self._dataset_view.setModel(self._dataset_model)
        # self._dataset_model.dataChanged.connect(self._dataset_view.update)
        self._sample_view = qtw.QListView()
        self._sample_view.setModel(self._sample_model)
        self._refit_button = qtw.QPushButton("Refit pipeline")

        self.main_widget = MainWidget()
        self.main_widget.set_document_view(self._pdf_view)
        self.main_widget.add_page(self._dataset_view, "Dataset")
        self.main_widget.add_page(self._sample_view, "Sample")
        self.main_widget.add_page(self._refit_button, "Pipeline")

        self.main_window = MainWindow()
        self.main_window.setCentralWidget(self.main_widget)
        window_width, _ = self.main_window.set_default_geometry()
        self.main_widget.setSizes([int(0.5 * window_width), int(0.5 * window_width)])

        self.main_window.import_sample_requested.connect(self.import_sample)
        self.main_window.import_context_requested.connect(self.import_context)
        #self.main_window.import_pipeline_requested.connect(self.import_pipeline)
        #self.main_window.import_preproc_requested.connect(self.import_preproc)
        self.main_window.new_dataset_requested.connect(self.new_dataset)
        self.main_window.open_dataset_requested.connect(self.open_dataset)
        self.main_window.save_dataset_requested.connect(self.save_dataset)
        self.main_widget.next_document_requested.connect(self.next_document)
        self._refit_button.clicked.connect(self.refit_pipeline)

        self.main_window.show()

    def _is_safe_to_proceed(self) -> bool:
        if not self._dataset_model.is_saved():
            answer = qtw.QMessageBox.question(
                None,
                "Unsaved data",
                "Any unsaved data will be lost. Are you sure you want to proceed?",
                qtw.QMessageBox.Yes | qtw.QMessageBox.No,
            )
            return answer == qtw.QMessageBox.Yes
        return True

    @qtc.pyqtSlot(str)
    def import_sample(self, directorypath):
        # FIXME: Gracefully handle incorrect file paths
        files = [os.path.join(directorypath, f) for f in os.scandir(directorypath)]
        random.shuffle(files)
        self._sample_model.setStringList(files)
        self.next_document(None)

    @qtc.pyqtSlot(str)
    def import_preproc(self, filepath):
        if self._is_safe_to_proceed():
            self._preprocessor = joblib.load(filepath)

    @qtc.pyqtSlot(str)
    def import_context(self, filepath):
        if self._is_safe_to_proceed():
            self._context = joblib.load(filepath)

    @qtc.pyqtSlot(str)
    def import_pipeline(self, filepath):
        if self._is_safe_to_proceed():
            self._pipe = joblib.load(filepath)

    @qtc.pyqtSlot()
    def new_dataset(self):
        if self._is_safe_to_proceed():
            self._dataset_model = DataframeTableModel()
            self._dataset_view.setModel(self._dataset_model)

    @qtc.pyqtSlot(str)
    def open_dataset(self, filepath):
        if self._is_safe_to_proceed():
            self._dataset_model = DataframeTableModel.load(filepath)
            self._dataset_view.setModel(self._dataset_model)

    @qtc.pyqtSlot(str)
    def save_dataset(self, filepath):
        self._dataset_model.save(filepath)

    @qtc.pyqtSlot(bool)
    def next_document(self, _):
        if self._sample_model.rowCount():
            documentpath = self._sample_model.pop()
            pdf = PyPDF2.PdfFileReader(documentpath)
            pages = [pdf.getPage(i).extractText() for i in range(pdf.getNumPages())]
            for i, pagetext in enumerate(pages):
                if self._context.preprocessor.accepts_page(pagetext):
                    pagetext = " ".join(pagetext.strip().split())
                    snippets = self._context.preprocessor.transform(pagetext)
                    try:
                        probas = self._context.pipeline.predict_proba(snippets)
                        classes = self._context.pipeline.predict(snippets)
                    except NotFittedError:
                        probas = [[0.5, 0.5]] * len(snippets)
                        classes = [0] * len(snippets)
                    spc = zip(snippets, probas, classes)
                    for snippet in spc:
                        self._dataset_model.appendRow(
                            documentpath, i + 1, snippet[0], snippet[1][1], snippet[2]
                        )
            self._dataset_view.scrollToBottom()
            self._pdf_view.load(documentpath)  # Not thread safe

    @qtc.pyqtSlot()
    def refit_pipeline(self):
        X = self._dataset_model.dataframe()["text"]
        y = pd.to_numeric(self._dataset_model.dataframe()["class"])
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.4, shuffle=True, random_state=RANDOM_STATE
            )
            self._context.pipeline.fit(X_train, y_train)
            y_predict = self._context.pipeline.predict(X_test)
            y_prob = self._context.pipeline.predict_proba(X_test)[:, 1]
            print(classification_report(y_test, y_predict))
            print(confusion_matrix(y_test, y_predict))
            fpr, tpr, thresholds = roc_curve(y_test, y_prob)
            roc_auc = auc(fpr, tpr)
            print("AUC:", roc_auc)
        except Exception as e:
            qtw.QMessageBox.warning(None, "Warning", repr(e))
        try:
            self._context.pipeline.fit(X, y)
        except Exception as e:
            qtw.QMessageBox.warning(None, "Warning", repr(e))

    def exec_(self):
        try:
            return super().exec_()
        except Exception as e:
            qtw.QMessageBox.critical(None, "Critical error", str(e))
            raise e
        finally:
            pass  # TODO: Implement workspace recovery
            return 1

    @classmethod
    def main(cls):
        app = cls(sys.argv)
        return app.exec_()


if __name__ == "__main__":
    sys.exit(MainApp.main())
