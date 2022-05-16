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

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class PandasTableModel(qtc.QAbstractTableModel):
    def __init__(self, df):
        super().__init__()
        self._df = pd.DataFrame()

    def appendRow(self, filename: str, page: int, target: str, class_: int):
        self.beginInsertRows(qtc.QModelIndex(), self.rowCount(), self.rowCount())
        self._df = self._df.append({"file": filename, "page": page, "target": target, "class": class_}, ignore_index=True) 
        self.endInsertRows()

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=qtc.Qt.DisplayRole):
        if index.isValid():
            if role == qtc.Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return self._df.columns[col]
        return None

    def setData(self, index, value, role=qtc.Qt.EditRole) -> bool:
        if role == qtc.Qt.EditRole:
            if not index.isValid():
                return False
            self._df.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [role])
            print(self._df)
            return True
        else:
            return False

    def flags(self, index):
        if index.column() == self._df.columns.get_loc("class"):
            return qtc.Qt.ItemIsEditable | super().flags(index)
        else:
            return super().flags(index)
            