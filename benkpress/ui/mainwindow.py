# Form implementation generated from reading ui file '.\benkpress\ui\mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(825, 591)
        self.main_widget = QtWidgets.QWidget(parent=MainWindow)
        self.main_widget.setObjectName("main_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.main_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_splitter = QtWidgets.QSplitter(parent=self.main_widget)
        self.main_splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.main_splitter.setObjectName("main_splitter")
        self.web_engine_view = PDFView(parent=self.main_splitter)
        self.web_engine_view.setObjectName("web_engine_view")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.main_splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setObjectName("sidebar_layout")
        self.tabs = QtWidgets.QTabWidget(parent=self.verticalLayoutWidget)
        self.tabs.setObjectName("tabs")
        self.dataset_tab = QtWidgets.QWidget()
        self.dataset_tab.setObjectName("dataset_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dataset_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.dataset = QtWidgets.QTableView(parent=self.dataset_tab)
        self.dataset.setObjectName("dataset")
        self.verticalLayout_3.addWidget(self.dataset)
        self.tabs.addTab(self.dataset_tab, "")
        self.sample_tab = QtWidgets.QWidget()
        self.sample_tab.setObjectName("sample_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.sample_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sample = QtWidgets.QListView(parent=self.sample_tab)
        self.sample.setObjectName("sample")
        self.verticalLayout_2.addWidget(self.sample)
        self.tabs.addTab(self.sample_tab, "")
        self.pipeline_tab = QtWidgets.QWidget()
        self.pipeline_tab.setObjectName("pipeline_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.pipeline_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.validation_results = QtWidgets.QPlainTextEdit(parent=self.pipeline_tab)
        self.validation_results.setObjectName("validation_results")
        self.verticalLayout_4.addWidget(self.validation_results)
        self.validation_settings_layout = QtWidgets.QFormLayout()
        self.validation_settings_layout.setObjectName("validation_settings_layout")
        self.kfold_splits = QtWidgets.QSpinBox(parent=self.pipeline_tab)
        self.kfold_splits.setObjectName("kfold_splits")
        self.validation_settings_layout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.kfold_splits)
        self.kfold_label = QtWidgets.QLabel(parent=self.pipeline_tab)
        self.kfold_label.setObjectName("kfold_label")
        self.validation_settings_layout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.kfold_label)
        self.verticalLayout_4.addLayout(self.validation_settings_layout)
        self.refit_pipeline = QtWidgets.QPushButton(parent=self.pipeline_tab)
        self.refit_pipeline.setObjectName("refit_pipeline")
        self.verticalLayout_4.addWidget(self.refit_pipeline)
        self.tabs.addTab(self.pipeline_tab, "")
        self.sidebar_layout.addWidget(self.tabs)
        self.next_document = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.next_document.setObjectName("next_document")
        self.sidebar_layout.addWidget(self.next_document)
        self.horizontalLayout.addWidget(self.main_splitter)
        MainWindow.setCentralWidget(self.main_widget)
        self.menu_bar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 825, 21))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_file = QtWidgets.QMenu(parent=self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        self.menu_help = QtWidgets.QMenu(parent=self.menu_bar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(parent=MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)
        self.action_about = QtGui.QAction(parent=MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_new_session = QtGui.QAction(parent=MainWindow)
        self.action_new_session.setObjectName("action_new_session")
        self.action_save_dataset = QtGui.QAction(parent=MainWindow)
        self.action_save_dataset.setObjectName("action_save_dataset")
        self.action_save_dataset_as = QtGui.QAction(parent=MainWindow)
        self.action_save_dataset_as.setObjectName("action_save_dataset_as")
        self.action_import_sample = QtGui.QAction(parent=MainWindow)
        self.action_import_sample.setObjectName("action_import_sample")
        self.action_exit = QtGui.QAction(parent=MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.actionExport_dataset = QtGui.QAction(parent=MainWindow)
        self.actionExport_dataset.setObjectName("actionExport_dataset")
        self.menu_file.addAction(self.action_new_session)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_save_dataset)
        self.menu_file.addAction(self.action_save_dataset_as)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_help.addAction(self.action_about)
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "benkpress2"))
        self.tabs.setTabText(self.tabs.indexOf(self.dataset_tab), _translate("MainWindow", "Dataset"))
        self.tabs.setTabText(self.tabs.indexOf(self.sample_tab), _translate("MainWindow", "Sample"))
        self.kfold_label.setText(_translate("MainWindow", "K-fold splits"))
        self.refit_pipeline.setText(_translate("MainWindow", "Refit pipeline"))
        self.tabs.setTabText(self.tabs.indexOf(self.pipeline_tab), _translate("MainWindow", "Pipeline"))
        self.next_document.setText(_translate("MainWindow", ">>> Next document >>>"))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.menu_help.setTitle(_translate("MainWindow", "Help"))
        self.action_about.setText(_translate("MainWindow", "About"))
        self.action_new_session.setText(_translate("MainWindow", "New session"))
        self.action_save_dataset.setText(_translate("MainWindow", "Save dataset"))
        self.action_save_dataset_as.setText(_translate("MainWindow", "Save dataset as"))
        self.action_import_sample.setText(_translate("MainWindow", "Import sample"))
        self.action_exit.setText(_translate("MainWindow", "Exit"))
        self.actionExport_dataset.setText(_translate("MainWindow", "Export dataset"))
from benkpress.widget.pdfview import PDFView
