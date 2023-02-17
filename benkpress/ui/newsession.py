# Form implementation generated from reading ui file '.\benkpress\ui\newsession.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_NewSessionDialog(object):
    def setupUi(self, NewSessionDialog):
        NewSessionDialog.setObjectName("NewSessionDialog")
        NewSessionDialog.resize(464, 617)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewSessionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.general_settings = QtWidgets.QGroupBox(parent=NewSessionDialog)
        self.general_settings.setObjectName("general_settings")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.general_settings)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=self.general_settings)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.sample_folder = PathEdit(parent=self.general_settings)
        self.sample_folder.setProperty("folder", True)
        self.sample_folder.setObjectName("sample_folder")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.sample_folder)
        self.label_2 = QtWidgets.QLabel(parent=self.general_settings)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.page_filter = PageFilterBox(parent=self.general_settings)
        self.page_filter.setObjectName("page_filter")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.page_filter)
        self.label_3 = QtWidgets.QLabel(parent=self.general_settings)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.pipeline = PipelineBox(parent=self.general_settings)
        self.pipeline.setObjectName("pipeline")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.pipeline)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.file_target = QtWidgets.QRadioButton(parent=self.general_settings)
        self.file_target.setObjectName("file_target")
        self.target = QtWidgets.QButtonGroup(NewSessionDialog)
        self.target.setObjectName("target")
        self.target.addButton(self.file_target)
        self.verticalLayout_4.addWidget(self.file_target)
        self.page_target = QtWidgets.QRadioButton(parent=self.general_settings)
        self.page_target.setObjectName("page_target")
        self.target.addButton(self.page_target)
        self.verticalLayout_4.addWidget(self.page_target)
        self.sentence_target = QtWidgets.QRadioButton(parent=self.general_settings)
        self.sentence_target.setChecked(True)
        self.sentence_target.setObjectName("sentence_target")
        self.target.addButton(self.sentence_target)
        self.verticalLayout_4.addWidget(self.sentence_target)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.verticalLayout_4)
        self.label_6 = QtWidgets.QLabel(parent=self.general_settings)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        self.spacy_model = SpacyModelsBox(parent=self.general_settings)
        self.spacy_model.setObjectName("spacy_model")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spacy_model)
        self.label_7 = QtWidgets.QLabel(parent=self.general_settings)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_7)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.verticalLayout.addWidget(self.general_settings)
        self.pdf_reader_settings = QtWidgets.QGroupBox(parent=NewSessionDialog)
        self.pdf_reader_settings.setObjectName("pdf_reader_settings")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.pdf_reader_settings)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(parent=self.pdf_reader_settings)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(parent=self.pdf_reader_settings)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.poppler_dpi = QtWidgets.QSpinBox(parent=self.pdf_reader_settings)
        self.poppler_dpi.setMinimum(72)
        self.poppler_dpi.setMaximum(300)
        self.poppler_dpi.setSingleStep(10)
        self.poppler_dpi.setProperty("value", 120)
        self.poppler_dpi.setObjectName("poppler_dpi")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.poppler_dpi)
        self.reader = ReaderBox(parent=self.pdf_reader_settings)
        self.reader.setObjectName("reader")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.reader)
        self.poppler_path = PathEdit(parent=self.pdf_reader_settings)
        self.poppler_path.setProperty("folder", True)
        self.poppler_path.setObjectName("poppler_path")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.poppler_path)
        self.tesseract_path = PathEdit(parent=self.pdf_reader_settings)
        self.tesseract_path.setObjectName("tesseract_path")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tesseract_path)
        self.label_8 = QtWidgets.QLabel(parent=self.pdf_reader_settings)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_8)
        self.label_9 = QtWidgets.QLabel(parent=self.pdf_reader_settings)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_9)
        self.label_10 = QtWidgets.QLabel(parent=self.pdf_reader_settings)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_10)
        self.tesseract_language = QtWidgets.QLineEdit(parent=self.pdf_reader_settings)
        self.tesseract_language.setObjectName("tesseract_language")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tesseract_language)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.verticalLayout.addWidget(self.pdf_reader_settings)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=NewSessionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NewSessionDialog)
        QtCore.QMetaObject.connectSlotsByName(NewSessionDialog)

    def retranslateUi(self, NewSessionDialog):
        _translate = QtCore.QCoreApplication.translate
        NewSessionDialog.setWindowTitle(_translate("NewSessionDialog", "New session"))
        self.general_settings.setTitle(_translate("NewSessionDialog", "General Settings"))
        self.label.setText(_translate("NewSessionDialog", "Sample folder"))
        self.label_2.setText(_translate("NewSessionDialog", "Page filter"))
        self.label_3.setText(_translate("NewSessionDialog", "Pipeline"))
        self.file_target.setText(_translate("NewSessionDialog", "File"))
        self.page_target.setText(_translate("NewSessionDialog", "Page"))
        self.sentence_target.setText(_translate("NewSessionDialog", "Sentence"))
        self.label_6.setText(_translate("NewSessionDialog", "Target"))
        self.label_7.setText(_translate("NewSessionDialog", "Spacy model"))
        self.pdf_reader_settings.setTitle(_translate("NewSessionDialog", "PDF Reader Settings"))
        self.label_4.setText(_translate("NewSessionDialog", "Reader"))
        self.label_5.setText(_translate("NewSessionDialog", "DPI"))
        self.label_8.setText(_translate("NewSessionDialog", "Language"))
        self.label_9.setText(_translate("NewSessionDialog", "Poppler path"))
        self.label_10.setText(_translate("NewSessionDialog", "Tesseract path"))
        self.tesseract_language.setText(_translate("NewSessionDialog", "eng"))
from benkpress.widget import PageFilterBox, PathEdit, PipelineBox, ReaderBox, SpacyModelsBox
