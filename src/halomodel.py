from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex


class MyNode(object):

    def __init__(self, name, state, description, parent=None):
        self.data = {
            'Foo': name,
            'Bar': state,
            'Baz': description
        }
        self.parent = parent
        self.children = []
        self.setParent(parent)

    def setParent(self, parent):
        if parent is not None:
            self.parent = parent
            self.parent.appendChild(self)
        else:
            self.parent = None

    def appendChild(self, child):
        self.children.append(child)

    def childAtRow(self, row):
        return self.children[row]

    def rowOfChild(self, child):
        for i, item in enumerate(self.children):
            if item == child:
                return i
        return -1

    def removeChild(self, row):
        value = self.children[row]
        self.children.remove(value)

        return True

    def __len__(self):
        return len(self.children)


class HaloModel(QAbstractItemModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.treeview = kwargs.get('parent')
        self.headers = ['Foo', 'Bar', 'Baz']
        self.columns = len(self.headers)
        self.load_model()

    def load_model(self):
        self.root = MyNode('root', None, 'I am root', None)
        itemA = MyNode('itemA', None, 'this is item A', self.root)
        itemA1 = MyNode('itemA1', 'on', 'this is item A1', itemA)

        itemB = MyNode('itemB', 'on', 'this is item B', self.root)
        itemB1 = MyNode('itemB1', 'on', 'this is item B1', itemB)

        itemC = MyNode('itemC', 'on', 'this is item C', self.root)
        itemC1 = MyNode('itemC1', 'on', 'this is item C1', itemC)

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
        if role == Qt.DecorationRole:
            return None
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignTop | Qt.AlignLeft)

        if role != Qt.DisplayRole:
            return None

        node = self.nodeFromIndex(index)
        return node.data[self.headers[index.column()]]

    def setData(self, index, value, role):
        node = self.nodeFromIndex(index)
        node.data[self.headers[index.column()]] = value
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
