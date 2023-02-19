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

import sys
from hashlib import md5
from pathlib import Path
from typing import List

import PyQt6.QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

from benkpress.api.reader import Reader
from benkpress.datamodel import DataframeTableModel, SampleStringStackModel, Session
from benkpress.plugin import PluginLoader
from benkpress.ui.mainwindow import Ui_MainWindow
from benkpress.ui.newsession import Ui_NewSessionDialog


class MainWindow(qtw.QMainWindow):
    """The main window of the application."""

    new_session_requested = qtc.pyqtSignal()
    quit_requested = qtc.pyqtSignal()
    session: Session

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_ui()
        self._init_connections()
        self._init_models()

    def _init_ui(self):
        """Initialize the user interface."""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def _init_connections(self):
        """Initialize connections between signals and slots."""
        # TODO: Should consider dataset save state before most of these actions.
        self.ui.new_session_action.triggered.connect(self.request_new_session)
        self.ui.exit_action.triggered.connect(self.quit_requested.emit)

        self.ui.next_document_button.clicked.connect(self.next_document)

    def _init_models(self):
        """Initialize the application models."""
        self.sample = SampleStringStackModel()
        self.dataset = DataframeTableModel()

    @qtc.pyqtSlot()
    def request_new_session(self):
        # TODO: Should consider dataset save state before this action.
        self.new_session_requested.emit()

    @qtc.pyqtSlot()
    def show_save_dataset_dialog(self):
        filename, _ = qtw.QFileDialog.getSaveFileName(
            caption="Save dataset",
            filter="All files (*.*);;Comma separated values (*.csv)",
            initialFilter="Comma separated values (*.csv)",
        )
        if filename:
            ...
            # self.save_dataset_requested.emit(filename)

    def set_session(self, session: Session):
        """Set the current session."""
        self.session = session
        self.ui.sample_list_view.setModel(self.session.sample)
        self.ui.dataset_table_view.setModel(self.session.dataset)

    @qtc.pyqtSlot(bool)
    def next_document(self, _):
        if not self.session.sample.rowCount():
            return
        # Step 1: Read
        documentpath = Path(self.session.sample.pop())
        read_pages = self.session.reader.read(documentpath)
        file_id = md5(documentpath.name.encode()).hexdigest()
        filtered_pages = []

        for i, page_text in enumerate(read_pages):
            if self.session.page_filter.predict([page_text])[0]:
                filtered_pages.append((i + 1, page_text))

        print(filtered_pages)


        # Step 2: Preprocess
        if self.session.target == Session.Target.FILE:
            pages = [" ".join(pages)]

        # Step 3: Prepare rows
        for page, page_text in enumerate(pages):
            if self.session.target == Session.Target.SENTENCE:

            # FIXME: Continue from here

            self.session.dataset.appendRow(
                md5(documentpath.name.encode()).hexdigest(),
                document + 1,
                document_text,
                0.5,
                0,
            )

        # Step 4: Predict
        # for i, pagetext in enumerate(self._reader.read(Path(documentpath))):
        #    if self._preprocessor.accepts_page(pagetext):
        #        pagetext = " ".join(pagetext.strip().split())
        #        snippets = self._preprocessor.transform(pagetext)
        # try:
        #    if not self._pipeline:
        #        raise NotFittedError
        #    probas = self._pipeline.predict_proba(snippets)
        #    classes = self._pipeline.predict(snippets)
        # except NotFittedError:
        #    probas = [[0.5, 0.5]] * len(snippets)
        #    classes = [0] * len(snippets)
        # spc = zip(snippets, probas, classes)
        # for snippet in spc:
        #     self._dataset_model.appendRow(
        #         documentpath, i + 1, snippet[0], snippet[1][1], snippet[2]
        #    )
        self.ui.dataset_table_view.scrollToBottom()
        self.ui.pdf_view.load(str(documentpath))  # Not thread safe


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
    """The main application object."""

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
        self.main_window.new_session_requested.connect(self._open_new_session_dialog)
        self.main_window.quit_requested.connect(self.quit)
        self.new_session_dialog.session_created.connect(self.main_window.set_session)

    def _open_new_session_dialog(self):
        """Open the new session dialog."""
        self.new_session_dialog.open()


def main():
    """The main application entrypoint."""
    return Application(sys.argv).exec()


if __name__ == "__main__":
    sys.exit(main())
