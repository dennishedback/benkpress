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

class TargetsModel(qtc.QAbstractTableModel):
    def __init__(self, targets):
        qtc.QAbstractTableModel.__init__(self)
        self._targets = targets

    def addRow(self, target: str, class_: int):
        self._targets.append({"target": target, "class": class_}, ignore_index=True) 
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return self._targets.shape[0]

    def columnCount(self, parent=None):
        return self._targets.shape[1]

    def data(self, index, role=qtc.Qt.DisplayRole):
        if index.isValid():
            if role == qtc.Qt.DisplayRole:
                return str(self._targets.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return self._targets.columns[col]
        return None

class TargetsView(qtw.QTableView):
    @qtc.pyqtSlot()
    def refresh(self):
        self.update()
