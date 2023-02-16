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

from dataclasses import dataclass
from enum import Enum
from typing import Any

import pandas as pd
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from sklearn.pipeline import Pipeline

from benkpress.api.reader import Reader


@dataclass
class Session:
    """Describes a tagging session of the application."""

    class Target(Enum):
        """Describes the target of a tagging session."""

        FILE = 1
        PAGE = 2
        SENTENCE = 3

    target: Target
    dataset: DataframeTableModel
    sample: SampleStringStackModel
    pipeline: Pipeline
    page_filter: Pipeline
    reader: Reader


class SampleStringStackModel(qtc.QStringListModel):
    def __init__(self):
        super().__init__()

    def pop(self) -> str:
        index = self.createIndex(0, 0)
        item = self.itemData(index)
        self.removeRows(0, 1)
        return item[0]


class DataframeTableModel(qtc.QAbstractTableModel):
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
