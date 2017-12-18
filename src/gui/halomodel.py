from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
from nimbus import HaloMap

from .icons import get_icon
from .treenode import WorkbenchNode, MapNode


class HaloModel(QAbstractItemModel):

    def __init__(self, map_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.treeview = kwargs.get('parent')
        self.headers = [None, 'Type', 'Value']
        self.columns = len(self.headers)
        self.root = WorkbenchNode()

        # Load map
        MapNode(HaloMap.from_file(map_path), self.root)

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def flags(self, index):
        defaultFlags = QAbstractItemModel.flags(self, index)
        if index.isValid():
            return (
                Qt.ItemIsEditable |
                Qt.ItemIsDragEnabled |
                Qt.ItemIsDropEnabled |
                defaultFlags)
        else:
            return Qt.ItemIsDropEnabled | defaultFlags

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()
        return True

    def index(self, row, column, parent):
        node = self.nodeFromIndex(parent)
        return self.createIndex(row, column, node.childAtRow(row))

    def columnCount(self, parent):
        return self.columns

    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None:
            return 0
        return len(node)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return QAbstractItemModel.headerData(self, section, orientation, role)

    def data(self, index, role):
        node = self.nodeFromIndex(index)
        column = index.column()

        if role == Qt.DecorationRole and column == 0:
            return get_icon()

        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignTop | Qt.AlignLeft)

        if role != Qt.DisplayRole:
            return None

        return node.display(column)

    def setData(self, index, value, role):
        # node = self.nodeFromIndex(index)
        # node.data[self.headers[index.column()]] = value
        return True

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()

        node = self.nodeFromIndex(child)
        if node is None:
            return QModelIndex()

        parent = node.parent
        if parent is None:
            return QModelIndex()

        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.rowOfChild(parent)

        assert row != - 1
        return self.createIndex(row, 0, parent)

    def nodeFromIndex(self, index):
        return index.internalPointer() if index.isValid() else self.root
