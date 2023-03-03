# benkpress
# Copyright (C) 2022-2023 Dennis Hedback
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

"""Module containing the application class as well as top-level windows and dialogs."""

import io
import logging
import sys
from hashlib import md5
from pathlib import Path
from typing import List

import PyQt6.QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw
from sklearn.exceptions import NotFittedError
from sklearn.metrics import auc, classification_report, confusion_matrix, roc_curve
from sklearn.model_selection import KFold

from benkpress.datamodel import DataframeTableModel, Session
from benkpress.plugin import PluginLoader
from benkpress.resources import QUICK_START_GUIDE_PATH
from benkpress.ui.mainwindow import Ui_MainWindow
from benkpress.ui.newsession import Ui_NewSessionDialog

logger = logging.getLogger(__name__)


class MainWindow(qtw.QMainWindow):
    """The main window of the application."""

    new_session_requested = qtc.pyqtSignal()
    save_dataset_requested = qtc.pyqtSignal(Session)
    quit_requested = qtc.pyqtSignal()
    session: Session = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_ui()
        self._init_connections()

    def _init_ui(self):
        """Initialize the user interface."""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pdf_view.load(str(QUICK_START_GUIDE_PATH))

    def _init_connections(self):
        """Initialize connections between signals and slots."""
        # TODO: Should consider dataset save state before most of these actions.
        self.ui.new_session_action.triggered.connect(self.request_new_session)
        self.ui.save_dataset_action.triggered.connect(self.request_save_dataset)
        self.ui.exit_action.triggered.connect(self.request_quit)

        self.ui.next_document_button.clicked.connect(self.next_document)
        self.ui.refit_pipeline_button.clicked.connect(self.refit_pipeline)

    def session_needs_saving(self) -> bool:
        has_session = self.session is not None
        if has_session:
            return not self.session.dataset.is_saved()
        return False

    @qtc.pyqtSlot()
    def request_new_session(self):
        self.new_session_requested.emit()

    @qtc.pyqtSlot()
    def request_save_dataset(self):
        self.save_dataset_requested.emit(self.session)

    @qtc.pyqtSlot()
    def request_quit(self):
        self.quit_requested.emit()

    def set_session(self, session: Session):
        """Set the current session."""
        self.session = session
        self.ui.sample_list_view.setModel(self.session.sample)
        self.ui.dataset_table_view.setModel(self.session.dataset)

    @qtc.pyqtSlot(bool)
    def next_document(self, _):
        if (
            not self.session.sample.rowCount()
        ):  # TODO: The name of the method called here should be more informative.
            return

        # Step 1: Read
        documentpath = Path(self.session.sample.pop())
        read_pages = self.session.reader.read(documentpath)
        file_id = md5(documentpath.name.encode()).hexdigest()
        filtered_pages = []

        # Step 2: Filter pages
        for i, page_text in enumerate(read_pages):
            if self.session.page_filter.predict([page_text])[0]:
                page_number = i + 1
                filtered_pages.append((page_number, page_text))

        # Step 3: Preprocess documents
        if self.session.target == Session.Target.FILE:
            filtered_documents = [
                (0, " ".join([page_text for _, page_text in filtered_pages]))
            ]
        elif self.session.target == Session.Target.SENTENCE:
            filtered_documents = [
                (page_number, sentence)
                for page_number, page_text in filtered_pages
                for sentence in self.session.sentencizer.sentencize(page_text)
            ]
        else:  # Session.Target.PAGE
            filtered_documents = filtered_pages

        # Step 4: Predict and add to dataset
        for page_number, document_text in filtered_documents:
            try:
                if not self.session.pipeline:
                    raise NotFittedError
                proba = self.session.pipeline.predict_proba([document_text])[0][1]
                class_ = self.session.pipeline.predict([document_text])[0]
            except NotFittedError:
                proba = 0.0
                class_ = 0
            self.session.dataset.appendRow(
                DataframeTableModel.RowConfig(
                    file_id, page_number, document_text, proba, class_
                )
            )

        # Step 5: Update UI
        self.ui.dataset_table_view.scrollToBottom()
        self.ui.pdf_view.load(str(documentpath))  # Not thread safe

    # TODO: The following private methods should be part of the
    # widget rather than the main window.

    def _print_to_string(self, *args, **kwargs):
        with io.StringIO() as sstream:
            print(*args, file=sstream, **kwargs)
            return sstream.getvalue()

    def _print_to_benchmark_view(self, performance_metrics: str):
        current_output = self.ui.validation_results_view.toPlainText()
        self.ui.validation_results_view.setPlainText(
            current_output + self._print_to_string(performance_metrics) + "\n"
        )

    def _flush_benchmark_view(self):
        current_output = self.ui.validation_results_view.toPlainText()
        current_output += "\n\n"
        current_output += "============================================================"
        current_output += "\n\n"
        self.ui.validation_results_view.setPlainText(current_output)

    def _scroll_down_benchmark_view(self):
        self.ui.validation_results_view.verticalScrollBar().setSliderPosition(
            self.ui.validation_results_view.verticalScrollBar().maximum()
        )

    @qtc.pyqtSlot(bool)
    def refit_pipeline(self, _):
        X = self.session.dataset.texts()
        y = self.session.dataset.classes()
        try:
            num_splits = self.ui.kfold_splits_spin_box.value()
            self._flush_benchmark_view()
            self._print_to_benchmark_view(
                "# BENCHMARKS FOR %i-FOLD VALIDATION" % num_splits
            )
            # TODO: Should be able to configure the random state using
            # the GUI. Both here and in pipelines.
            ss = KFold(n_splits=num_splits, shuffle=True)
            for i, indices in enumerate(ss.split(X, y)):
                train_indices, test_indices = indices
                X_train = X[train_indices]
                y_train = y[train_indices]
                X_test = X[test_indices]
                y_test = y[test_indices]

                self.session.pipeline.fit(X_train, y_train)
                y_predict = self.session.pipeline.predict(X_test)
                y_prob = self.session.pipeline.predict_proba(X_test)[:, 1]
                fpr, tpr, _ = roc_curve(y_test, y_prob)
                roc_auc = auc(fpr, tpr)

                # TODO: Precision and f-score are ill-defined for labels with no
                # predicted samples. Should explicitly set the behaviour of these
                # metrics by passing the `zero_division` argument.

                self._print_to_benchmark_view("## Benchmark for fold %i" % (i + 1))
                self._print_to_benchmark_view("Accuracy, precision, recall:")
                self._print_to_benchmark_view(classification_report(y_test, y_predict))
                self._print_to_benchmark_view("Confusion matrix:")
                self._print_to_benchmark_view(confusion_matrix(y_test, y_predict))
                self._print_to_benchmark_view("AUROC:")
                self._print_to_benchmark_view(str(roc_auc))

                self._scroll_down_benchmark_view()

        except Exception as e:
            qtw.QMessageBox.warning(None, "Warning", repr(e))
        try:
            self.session.pipeline.fit(X, y)
        except Exception as e:
            qtw.QMessageBox.warning(None, "Warning", repr(e))


class NewSessionDialog(qtw.QDialog):
    """The dialog for creating a new tagging session."""

    ORGANIZATION: str = "dennishedback"
    APPLICATION: str = "benkpress2"

    session_created = qtc.pyqtSignal(Session)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_ui()
        self._init_connections()
        self._load_settings()
        self._plugin_loader = PluginLoader()

    def _init_ui(self):
        """Initialize the user interface."""
        self.ui = Ui_NewSessionDialog()
        self.ui.setupUi(self)

    def _init_connections(self):
        """Initialize connections between signals and slots."""
        self.ui.dialog_button_box.accepted.connect(self._on_accept_button_clicked)
        self.ui.dialog_button_box.accepted.connect(self.accept)
        self.ui.dialog_button_box.rejected.connect(self.reject)
        self.ui.reader_combo_box.currentTextChanged.connect(self._on_reader_changed)

    @qtc.pyqtSlot(str)
    def _on_reader_changed(self, text: str):
        """Handle a change in the PDF reader selection."""
        # TODO: Decouple this method from knowledge about reader module internals.
        # In particular, strings like "Tesseract" and "PyPDF" should be removed.
        # Perhaps the reader module should provide a list of available readers,
        # maybe as plugins, like the filters and pipelines. In any case, this
        # method should not be aware of the internals of the reader module.
        tesseract_settings_enabled = text == "Tesseract"
        self.ui.poppler_dpi_spin_box.setEnabled(tesseract_settings_enabled)
        self.ui.tesseract_language_line_edit.setEnabled(tesseract_settings_enabled)
        self.ui.poppler_path_line_edit.setEnabled(tesseract_settings_enabled)
        self.ui.tesseract_path_line_edit.setEnabled(tesseract_settings_enabled)

    @qtc.pyqtSlot()
    def _on_accept_button_clicked(self):
        """Handle the accept button being clicked."""
        self._create_session()
        self._save_settings()

    def _create_session(self):
        """Create a new session from the dialog's settings."""
        try:
            session = (
                Session.Builder()
                .log_stream()
                .sample(self.ui.sample_folder_path_line_edit.text())
                .page_filter(self.ui.page_filter_combo_box.currentText())
                .pipeline(self.ui.pipeline_combo_box.currentText())
                .target(self.ui.target_button_group.checkedButton().text())
                .sentencizer(self.ui.spacy_model_combo_box.currentText())
                .reader(
                    self.ui.reader_combo_box.currentText(),
                    self.ui.poppler_dpi_spin_box.value(),
                    self.ui.tesseract_language_line_edit.text(),
                    self.ui.poppler_path_line_edit.text(),
                    self.ui.tesseract_path_line_edit.text(),
                )
            ).build()
            self.session_created.emit(session)
        except Exception as e:
            qtw.QMessageBox.warning(
                self, "Error", f"An error occured while creating the session: {str(e)}"
            )

    # TODO: Currently the settings live in the registry on Windows through the use
    # of QSettings. This is not ideal, since we are already using userdirs for the
    # pdfjs files, thus fragmenting the application data. We should probably use a
    # single place for the settings instead.

    def _load_target_settings(self, settings: qtc.QSettings):
        buttons = self.ui.target_button_group.buttons()
        for button in buttons:
            if button.text() == settings.value("target"):
                button.setChecked(True)

    def _load_settings(self):
        """Load the dialog's settings."""
        settings = qtc.QSettings(self.ORGANIZATION, self.APPLICATION)
        if settings.contains("sample_folder"):
            self.ui.sample_folder_path_line_edit.setText(
                settings.value("sample_folder")
            )
        if settings.contains("page_filter"):
            self.ui.page_filter_combo_box.setCurrentText(settings.value("page_filter"))
        if settings.contains("pipeline"):
            self.ui.pipeline_combo_box.setCurrentText(settings.value("pipeline"))
        if settings.contains("target"):
            self._load_target_settings(settings)
        if settings.contains("sentencizer"):
            self.ui.spacy_model_combo_box.setCurrentText(settings.value("sentencizer"))
        if settings.contains("reader"):
            self.ui.reader_combo_box.setCurrentText(settings.value("reader"))
        if settings.contains("poppler_dpi"):
            self.ui.poppler_dpi_spin_box.setValue(settings.value("poppler_dpi"))
        if settings.contains("tesseract_language"):
            self.ui.tesseract_language_line_edit.setText(
                settings.value("tesseract_language")
            )
        if settings.contains("poppler_path"):
            self.ui.poppler_path_line_edit.setText(settings.value("poppler_path"))
        if settings.contains("tesseract_path"):
            self.ui.tesseract_path_line_edit.setText(settings.value("tesseract_path"))

    def _save_settings(self):
        """Save the dialog's settings."""
        settings = qtc.QSettings(self.ORGANIZATION, self.APPLICATION)
        settings.setValue("sample_folder", self.ui.sample_folder_path_line_edit.text())
        settings.setValue("page_filter", self.ui.page_filter_combo_box.currentText())
        settings.setValue("pipeline", self.ui.pipeline_combo_box.currentText())
        settings.setValue("target", self.ui.target_button_group.checkedButton().text())
        settings.setValue("sentencizer", self.ui.spacy_model_combo_box.currentText())
        settings.setValue("reader", self.ui.reader_combo_box.currentText())
        settings.setValue("poppler_dpi", self.ui.poppler_dpi_spin_box.value())
        settings.setValue(
            "tesseract_language", self.ui.tesseract_language_line_edit.text()
        )
        settings.setValue("poppler_path", self.ui.poppler_path_line_edit.text())
        settings.setValue("tesseract_path", self.ui.tesseract_path_line_edit.text())


class Application(qtw.QApplication):
    """The main application object. Responsible for creation of
    all windows and dialogs, as well as for the communication and
    coupling between those windows and dialogs."""

    main_window: MainWindow
    new_session_dialog: NewSessionDialog

    def __init__(self, argv: List[str]):
        super().__init__(argv)
        self._init_windows()
        self._init_connections()

    def _init_windows(self):
        """Initialize the application windows and dialogs."""
        self.main_window = MainWindow()
        self.main_window.show()
        self.new_session_dialog = NewSessionDialog(parent=self.main_window)

    def _init_connections(self):
        """Initialize connections between signals and slots."""
        self.main_window.new_session_requested.connect(self.open_new_session_dialog)
        self.main_window.quit_requested.connect(self.request_quit)
        self.new_session_dialog.session_created.connect(self.main_window.set_session)
        self.main_window.save_dataset_requested.connect(self.show_save_dataset_dialog)

    def _show_confirmation_dialog(self) -> bool:
        answer = qtw.QMessageBox.question(
            self.main_window,
            "Unsaved data",
            "Any unsaved data will be lost. Are you sure you want to proceed?",
            qtw.QMessageBox.StandardButton.Yes | qtw.QMessageBox.StandardButton.No,
        )
        return answer == qtw.QMessageBox.StandardButton.Yes

    def _user_wants_to_continue(self) -> bool:
        logger.debug("Checking if session needs saving")
        if self.main_window.session_needs_saving():
            logger.debug("Session needs saving")
            return self._show_confirmation_dialog()
        return True

    @qtc.pyqtSlot()
    def open_new_session_dialog(self):
        """Open the new session dialog."""
        if self._user_wants_to_continue():
            self.new_session_dialog.open()

    @qtc.pyqtSlot()
    def request_quit(self):
        """Request the application to quit."""
        if self._user_wants_to_continue():
            self.quit()

    @qtc.pyqtSlot(Session)
    def show_save_dataset_dialog(self, session: Session):
        # TODO: Implement saving of session metadata along with the dataset.
        filename, _ = qtw.QFileDialog.getSaveFileName(
            caption="Save dataset",
            filter="All files (*.*);;Comma separated values (*.csv)",
            initialFilter="Comma separated values (*.csv)",
        )
        if filename:
            session.dataset.save(filename)
            with open(f"{filename}.txt", "w") as f:
                f.write(session.log_stream.getvalue())


def main():
    """The main application entrypoint."""
    logging.basicConfig(level=logging.DEBUG)
    return Application(sys.argv).exec()


if __name__ == "__main__":
    sys.exit(main())
