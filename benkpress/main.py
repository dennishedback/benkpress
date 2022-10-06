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


import io
import os
import random
import sys

import PyPDF2
import pandas as pd
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from benkpress_plugins.preprocessors import Preprocessor
from sklearn.exceptions import NotFittedError
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline

from mainwidget import MainWidget
from mainwindow import MainWindow
from model import DataframeTableModel, SampleStringStackModel
from pdfjswebengineview import PDFJSWebEngineView
from pluginloader import PluginLoader

RANDOM_STATE = 999


class MainApp(qtw.QApplication):
    """The main application object."""

    _preprocessor: Preprocessor
    _pipeline: Pipeline

    def __init__(self, argv: List[str]):
        super().__init__(argv)

        # TODO: Should initalize all widgets in MainWidget and just connect everything
        # in this file.

        self._pipeline = None  # Should be some default value instead!
        self._preprocessor = None  # Should be some default value instead!

        self._plugin_loader = PluginLoader()

        self._pdf_view = PDFJSWebEngineView()
        self._dataset_model = DataframeTableModel()
        self._sample_model = SampleStringStackModel()

        self._dataset_view = qtw.QTableView()
        self._dataset_view.setModel(self._dataset_model)
        # self._dataset_model.dataChanged.connect(self._dataset_view.update)
        self._sample_view = qtw.QListView()
        self._sample_view.setModel(self._sample_model)

        self._benchmark_label = qtw.QLabel("Benchmark")
        self._benchmark_view = qtw.QPlainTextEdit()
        self._benchmark_view.setReadOnly(True)
        font = qtg.QFont("Monospace")
        font.setStyleHint(qtg.QFont.StyleHint.TypeWriter)
        self._benchmark_view.setFont(font)
        self._refit_button = qtw.QPushButton("Refit pipeline")

        self._kfold_spinbox = qtw.QSpinBox()
        self._kfold_spinbox.setMaximum(99)
        self._kfold_spinbox.setMinimum(0)
        self._kfold_spinbox.setValue(5)

        # self._threshold_spinbox = qtw.QDoubleSpinBox()
        # self._threshold_spinbox.setMaximum(1.0)
        # self._threshold_spinbox.setMinimum(0.0)
        # self._threshold_spinbox.setSingleStep(0.05)
        # self._threshold_spinbox.setValue(0.5)

        self._refit_settings_layout = qtw.QFormLayout()
        self._refit_settings_layout.addRow("K-fold splits", self._kfold_spinbox)
        # self._refit_settings_layout.addRow("Probability threshold", self._threshold_spinbox)

        self._refit_settings_widget = qtw.QWidget()
        self._refit_settings_widget.setLayout(self._refit_settings_layout)

        self._pipeline_layout = qtw.QVBoxLayout()
        self._pipeline_layout.addWidget(self._benchmark_label)
        self._pipeline_layout.addWidget(self._benchmark_view)
        self._pipeline_layout.addWidget(self._refit_settings_widget)
        self._pipeline_layout.addWidget(self._refit_button)
        self._pipeline_widget = qtw.QWidget()
        self._pipeline_widget.setLayout(self._pipeline_layout)

        self.main_widget = MainWidget()
        self.main_widget.set_document_view(self._pdf_view)
        self.main_widget.add_page(self._dataset_view, "Dataset")
        self.main_widget.add_page(self._sample_view, "Sample")
        self.main_widget.add_page(self._pipeline_widget, "Pipeline")

        self.main_window = MainWindow(self._plugin_loader)
        self.main_window.setCentralWidget(self.main_widget)
        window_width, _ = self.main_window.set_default_geometry()
        self.main_widget.setSizes([int(0.5 * window_width), int(0.5 * window_width)])

        self.main_window.import_sample_requested.connect(self.import_sample)
        self.main_window.change_preprocessor_requested.connect(self.change_preprocessor)
        self.main_window.change_pipeline_requested.connect(self.change_pipeline)
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
    def change_preprocessor(self, name: str):
        self._preprocessor = self._plugin_loader.load_preprocessor(name)

    @qtc.pyqtSlot(str)
    def change_pipeline(self, name: str):
        self._pipeline = self._plugin_loader.load_pipeline(name)

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
                if self._preprocessor.accepts_page(pagetext):
                    pagetext = " ".join(pagetext.strip().split())
                    snippets = self._preprocessor.transform(pagetext)
                    try:
                        probas = self._pipeline.predict_proba(snippets)
                        classes = self._pipeline.predict(snippets)
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

    def _print_to_string(self, *args, **kwargs):
        with io.StringIO() as sstream:
            print(*args, file=sstream, **kwargs)
            return sstream.getvalue()

    def _print_to_benchmark_view(self, performance_metrics: str):
        current_output = self._benchmark_view.toPlainText()
        self._benchmark_view.setPlainText(
            current_output + self._print_to_string(performance_metrics) + "\n")

    def _flush_benchmark_view(self):
        current_output = self._benchmark_view.toPlainText()
        current_output += "\n\n"
        current_output += "============================================================"
        current_output += "\n\n"
        self._benchmark_view.setPlainText(current_output)

    def _scroll_down_benchmark_view(self):
        self._benchmark_view.verticalScrollBar().setSliderPosition(
            self._benchmark_view.verticalScrollBar().maximum())

    @qtc.pyqtSlot()
    def refit_pipeline(self):
        X = self._dataset_model.dataframe()["text"]
        y = pd.to_numeric(self._dataset_model.dataframe()["class"])
        try:
            num_splits = self._kfold_spinbox.value()
            self._flush_benchmark_view()
            self._print_to_benchmark_view(
                "# BENCHMARKS FOR %i-FOLD VALIDATION" % num_splits)
            ss = KFold(n_splits=num_splits, shuffle=True, random_state=RANDOM_STATE)
            for i, indices in enumerate(ss.split(X, y)):
                train_indices, test_indices = indices
                X_train = X[train_indices]
                y_train = y[train_indices]
                X_test = X[test_indices]
                y_test = y[test_indices]

                self._pipeline.fit(X_train, y_train)
                y_predict = self._pipeline.predict(X_test)
                y_prob = self._pipeline.predict_proba(X_test)[:, 1]
                fpr, tpr, thresholds = roc_curve(y_test, y_prob)
                roc_auc = auc(fpr, tpr)

                self._print_to_benchmark_view("## Benchmark for fold %i" % (i + 1))
                self._print_to_benchmark_view("Accuracy, precision, recall:")
                self._print_to_benchmark_view(classification_report(y_test, y_predict))
                self._print_to_benchmark_view("Confusion matrix:")
                self._print_to_benchmark_view(
                    confusion_matrix(y_test, y_predict)
                )
                self._print_to_benchmark_view("AUROC:")
                self._print_to_benchmark_view(str(roc_auc))

                self._scroll_down_benchmark_view()

        except Exception as e:
            qtw.QMessageBox.warning(None, "Warning", repr(e))
        try:
            self._pipeline.fit(X, y)
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
