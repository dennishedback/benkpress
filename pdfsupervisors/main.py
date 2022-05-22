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

# TODO: Remove me

import random
import re
import os
import sys
from tracemalloc import stop
from typing import List

#from phdata.arlp.tokenize import WordSentTokenizer

sys.path.append(r"C:\Users\dhedb\Documents\Code\arlp")

import pandas as pd
import PyPDF2

from nltk.corpus import stopwords
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

# TODO: These should not be imported here, but used in external app
from sklearn.exceptions import NotFittedError
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
from xgboost import XGBClassifier
from imblearn.pipeline import Pipeline as ImbalancedPipe
from imblearn.over_sampling import SMOTE
import numpy as np

from api.preprocessor import PagePreprocessor
from mainwidget import MainWidget
from mainwindow import MainWindow
from model import DataframeTableModel, SampleStringStackModel
from pdfjswebengineview import PDFJSWebEngineView
from settings import get_user_data_path

from arlp.tokenize import SentenceTokenizer, WordSentTokenizer
from arlp.stemmer import AdvancedAuditReportSentStemmer

RANDOM_STATE = 999




class MainApp(qtw.QApplication):
    """The main application object."""

    def __init__(self, argv):
        super().__init__(argv)

        self._preprocessor = AuditReportPageFirstSentenceTargetPreprocessor()

        #transformer = StemTransformer()

        #df = pd.read_csv(r"C:\Users\dhedb\Desktop\test.csv")
        #print(df)
        #df["text"] = transformer.transform(df["text"])
        #print(df)
        #sys.exit()

        # The sentence classifier pipeline
        # self._pipe = ImbalancedPipe([
        #    ("stemmer", StemTransformer()),
        #    ("vectorizer", TfidfVectorizer(use_idf=True, ngram_range=(1, 2), max_features=None, stop_words=None)),
        #    ("resampler", SMOTE(sampling_strategy=0.5, random_state=RANDOM_STATE, n_jobs=-1)),
        #    ("xgboost", XGBClassifier(n_estimators=1000, random_state=RANDOM_STATE))
        # ])
        #self._pipe.fit(["godis", "fusk"], [0, 1])

        # The Big4 classifier pipeline
        self._pipe = Pipeline([
            ("vectorizer", TfidfVectorizer(use_idf=True, max_features=9999999, stop_words=stopwords.words("swedish"))),
            #("resampler", SMOTE(sampling_strategy=0.5, random_state=RANDOM_STATE, n_jobs=-1)),
            #("vectorizer", TfidfVectorizer(max_features=999999, stop_words=stopwords.words("swedish"))),
            ("xgboost", XGBClassifier(n_estimators=1000, random_state=RANDOM_STATE))
        ])

        self._pdf_view = PDFJSWebEngineView()
        self._dataset_model = DataframeTableModel()
        self._sample_model = SampleStringStackModel()

        self._dataset_view = qtw.QTableView()
        self._dataset_view.setModel(self._dataset_model)
        #self._dataset_model.dataChanged.connect(self._dataset_view.update)
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
        self.main_widget.setSizes([int(.5 * window_width), int(.5 * window_width)])

        self.main_window.import_sample_requested.connect(self.import_sample)
        self.main_window.new_dataset_requested.connect(self.new_dataset)
        self.main_window.open_dataset_requested.connect(self.open_dataset)
        self.main_window.save_dataset_requested.connect(self.save_dataset)
        self.main_widget.next_document_requested.connect(self.next_document)
        self._refit_button.clicked.connect(self.refit_pipeline)

        self.main_window.show()
        self.import_sample("E:\LFUppsats\lovisa_felicia")

    def _is_safe_to_proceed(self) -> bool:
        if not self._dataset_model.is_saved():
            answer = qtw.QMessageBox.question(
                None,
                "Unsaved data",
                "Any unsaved data will be lost. Are you sure you want to proceed?",
                qtw.QMessageBox.Yes | qtw.QMessageBox.No)
            return answer == qtw.QMessageBox.Yes
        return True

    @qtc.pyqtSlot(str)
    def import_sample(self, directorypath):
        # FIXME: Gracefully handle incorrect file paths
        files = [os.path.join(directorypath, f) for f in os.scandir(directorypath)]
        random.shuffle(files)
        self._sample_model.setStringList(files)
        self.next_document(None)

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
                    snippets = self._preprocessor.transform(pagetext)
                    try:
                        probas = self._pipe.predict_proba(snippets)
                        classes = self._pipe.predict(snippets)
                    except NotFittedError:
                        probas = [[.5, .5]] * len(snippets) 
                        classes = [0] * len(snippets)
                    spc = zip(snippets, probas, classes)
                    for snippet in spc:
                        self._dataset_model.appendRow(documentpath, i+1, snippet[0], snippet[1][1], snippet[2])
            self._dataset_view.scrollToBottom()
            self._pdf_view.load(documentpath)  # Not thread safe
    
    @qtc.pyqtSlot()
    def refit_pipeline(self):
        X = self._dataset_model.dataframe()["text"]
        y = pd.to_numeric(self._dataset_model.dataframe()["class"])
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.4, shuffle=True, random_state=RANDOM_STATE)
            self._pipe.fit(X_train, y_train)
            y_predict = self._pipe.predict(X_test)
            y_prob = self._pipe.predict_proba(X_test)[:, 1]
            print(classification_report(y_test, y_predict))
            print(confusion_matrix(y_test, y_predict))
            fpr, tpr, thresholds = roc_curve(y_test, y_prob)
            roc_auc = auc(fpr, tpr)
            print("AUC:", roc_auc)
        except Exception as e:
            qtw.QMessageBox.warning(None, "Warning", repr(e))
        try:
            self._pipe.fit(X, y)
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