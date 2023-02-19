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

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import pandas as pd
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from sklearn.pipeline import Pipeline

from benkpress.api.reader import PyPDFReader, Reader, TesseractReader
from benkpress.api.tokenizer import Sentencizer
from benkpress.plugin import PluginLoader


class SampleStringStackModel(qtc.QStringListModel):
    def __init__(self):
        super().__init__()

    def pop(self) -> str:
        index = self.createIndex(0, 0)
        item = self.itemData(index)
        self.removeRows(0, 1)
        return item[0]


class DataframeTableModel(qtc.QAbstractTableModel):
    """A table model for displaying a pandas dataframe."""

    # TODO: Consider deriving from QSortFilterProxyModel instead.
    # TODO: Establish consistent naming convention for table fields
    # across the application. For example, "page" vs "document".

    def __init__(self):
        super().__init__()
        self._df = pd.DataFrame()
        self._last_saved_rowcount = 0

    @classmethod
    def load(cls, filepath_or_buffer: Any) -> DataframeTableModel:
        model = cls()
        model._df = pd.read_csv(filepath_or_buffer, index_col=False)
        model._last_saved_rowcount = model.rowCount()
        return model

    def dataframe(self) -> pd.DataFrame:
        return self._df

    def is_saved(self) -> bool:
        # FIXME: Doesn't consider the contents of each row, only the number of rows.
        return self._last_saved_rowcount == self.rowCount()

    def save(self, filepath_or_buffer: Any) -> None:
        self._df["class"] = pd.to_numeric(self._df["class"])
        self._df.to_csv(filepath_or_buffer)
        self._last_saved_rowcount = self.rowCount()

    def appendRow(self, filename: str, page: int, text: str, proba: float, class_: int):
        self.beginInsertRows(qtc.QModelIndex(), self.rowCount(), self.rowCount())
        new_row = pd.DataFrame(
            {
                "file": filename,
                "page": page,
                "text": text,
                "proba": proba,
                "class": int(class_),
            },
            index=[0],
        )
        self._df = pd.concat([self._df.loc[:], new_row]).reset_index(drop=True)
        self.endInsertRows()
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=qtc.Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == qtc.Qt.ItemDataRole.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])
            elif role == qtc.Qt.ItemDataRole.ForegroundRole:
                if index.column() == self._df.columns.get_loc("proba"):
                    brush = qtg.QBrush()
                    brush.setColor(
                        qtg.QColor.fromRgb(
                            0,
                            int(
                                255.0
                                * float(self._df.iloc[index.row(), index.column()])
                            ),
                            0,
                        )
                    )
                    return brush
        return None

    def headerData(self, col, orientation, role):
        if (
            orientation == qtc.Qt.Orientation.Horizontal
            and role == qtc.Qt.ItemDataRole.DisplayRole
        ):
            if len(self._df.columns) > col:
                return self._df.columns[col]
        return None

    def setData(self, index, value, role=qtc.Qt.ItemDataRole.EditRole) -> bool:
        if role == qtc.Qt.ItemDataRole.EditRole:
            if not index.isValid():
                return False
            self._df.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    def flags(self, index):
        if index.column() == self._df.columns.get_loc("class"):
            return qtc.Qt.ItemFlag.ItemIsEditable | super().flags(index)
        else:
            return super().flags(index)


@dataclass
class Session:
    """Describes a tagging session of the application."""

    class Target(Enum):
        """Describes the target of a tagging session."""

        FILE = 1
        PAGE = 2
        SENTENCE = 3

    target: Target
    pipeline: Pipeline
    page_filter: Pipeline
    reader: Reader
    sentencizer: Sentencizer
    dataset: DataframeTableModel = field(default_factory=lambda: DataframeTableModel())
    sample: SampleStringStackModel = field(
        default_factory=lambda: SampleStringStackModel()
    )

    class Builder:
        """Builds a session object from raw input."""

        # TODO: This class might have too much responsibility. On the other hand
        # there is a trade-off between knowing how to create all these objects
        # and the amount of levels of indirection. Think about that.

        def __init__(self):
            self._plugin_loader = PluginLoader()
            self._sample = []
            self._target = None
            self._pipeline = None
            self._page_filter = None
            self._reader = None
            self._sentencizer = None

        def sample(self, sample_folder_name: str) -> Session.Builder:
            """Create a sample instance based on the given sample folder."""
            sample_folder = Path(sample_folder_name)
            self._sample_file_paths = [
                str(f) for f in sample_folder.iterdir() if f.is_file()
            ]
            random.shuffle(self._sample_file_paths)
            return self

        def target(self, target_name: str) -> Session.Builder:
            """Create a target instance based on the given target name."""
            self._target = Session.Target[target_name.upper()]
            print(self._target)
            return self

        def pipeline(self, pipeline_name: str) -> Session.Builder:
            """Create a pipeline instance based on the given pipeline name."""
            self._pipeline = self._plugin_loader.load_pipeline(pipeline_name)
            print(self._pipeline)
            return self

        def page_filter(self, page_filter_name: str) -> Session.Builder:
            """Create a page filter instance based on the given page filter name."""
            self._page_filter = self._plugin_loader.load_page_filter(page_filter_name)
            print(self._page_filter)
            return self

        def reader(
            self,
            reader_name: str,
            dpi: int,
            language: str,
            poppler_path: str,
            tesseract_path: str,
        ) -> Session.Builder:
            """Create a reader instance based on the given reader name and raw parameters."""
            # TODO: Decouple this method from knowledge about reader module internals.
            # In particular, strings like "Tesseract" and "PyPDF" should be removed.
            # Perhaps the reader module should provide a list of available readers,
            # maybe as plugins, like the filters and pipelines. In any case, this
            # method should not be aware of the internals of the reader module.
            if reader_name == "Tesseract":
                self._reader = TesseractReader(
                    tesseract_path=tesseract_path,
                    tesseract_language=language,
                    poppler_path=poppler_path,
                    dpi=dpi,
                )
            elif reader_name == "PyPDF":
                self._reader = PyPDFReader()
            else:
                raise ValueError(f"Unknown reader name: {reader_name}")
            print(self._reader)
            return self

        def sentencizer(self, model_name: str) -> Session.Builder:
            """Create a sentencizer instance based on the given model name."""
            self._sentencizer = Sentencizer(model_name)
            print(self._sentencizer)
            return self

        def build(self) -> Session:
            session = Session(
                target=self._target,
                pipeline=self._pipeline,
                page_filter=self._page_filter,
                reader=self._reader,
                sentencizer=self._sentencizer,
            )
            session.sample.setStringList(self._sample_file_paths)
            return session

    @classmethod
    def create_from_raw_input(cls):
        """Create a session object from raw input."""
        ...
