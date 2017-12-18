import abc
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
from nimbus import HaloMap
import os, sys

open_folder = None


def get_icon():
    global open_folder
    path = os.path.join(
        os.path.dirname(sys.modules[__name__].__file__),
        'gui',
        'open_folder.svg')
    if open_folder is None:
        open_folder = QtGui.QIcon()
        open_folder.addPixmap(
            QtGui.QPixmap(path),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
    return open_folder


class TreeNode(metaclass=abc.ABCMeta):

    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.setParent(parent)

    @abc.abstractmethod
    def display(self, column):
        pass

    @abc.abstractmethod
    def icon(self):
        get_icon()

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


class FieldNode(TreeNode):

    def __init__(self, fieldname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = fieldname

    def display(self, column):
        if column == 0:
            return self.name
        elif column == 1:
            return type(
                self.parent.hstruct.fields[self.name]).__name__
        elif column == 2:
            return getattr(self.parent.hstruct, self.name)

    def icon(self):
        return get_icon()


class StructNode(TreeNode):

    def __init__(self, name, hstruct, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.hstruct = hstruct
        if hstruct is not None:
            for fieldname in self.hstruct.fields.keys():
                FieldNode(fieldname, self)

    def display(self, column):
        if column == 0:
            return self.name
        elif column == 1:
            return 'Struct'

    def icon(self):
        return get_icon()


class TagNode(TreeNode):

    def __init__(self, htag, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.htag = htag
        StructNode('Header', htag.header, self)
        StructNode('Data', getattr(htag, 'data'), self)

    def display(self, column):
        if column == 0:
            return str(self.htag)[1:-1:]
        elif column == 1:
            return 'Tag'

    def icon(self):
        return get_icon()


tag_types = {
    'bipd': 'Biped',
    'bitm': 'Bitmap',
    'coll': 'Collision',
    'effe': 'Effect',
    'proj': 'Projectile',
    'weap': 'Weapon',
}


class TagTypeNode(TreeNode):

    def __init__(self, tag_type, tags, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_type = tag_type
        x = list(sorted(tags(tag_type)))
        self.count = len(x)
        for tag in x:
            TagNode(tag, self)

    def display(self, column):
        if column == 0:
            return '[{}] - {}'.format(
                self.tag_type,
                tag_types.get(self.tag_type, ''))
        elif column == 2:
            return self.count

    def icon(self):
        return get_icon()


class TagIndexNode(TreeNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def display(self, column):
        if column == 0:
            return 'tags'

    def icon(self):
        return get_icon()


class MapNode(TreeNode):

    def __init__(self, halomap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.halomap = halomap
        StructNode('map_header', halomap.map_header, self)
        StructNode('index_header', halomap.index_header, self)
        tag_index = TagIndexNode(self)
        for tag_type in sorted(self.halomap.tag_types):
            TagTypeNode(tag_type, self.halomap.tags, tag_index)

    def display(self, column):
        if column == 0:
            return self.halomap.map_header.map_name
        elif column == 1:
            return 'Map'

    def icon(self):
        return get_icon()


class WorkbenchNode(TreeNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def display(self, column):
        if column == 0:
            return 'Workbench'

    def icon(self):
        return get_icon()


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
