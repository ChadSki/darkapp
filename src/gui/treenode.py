import abc
from .icons import get_icon
from nimbus.tags import tag_names
from nimbus.halofield import StructArray


class TreeNode(metaclass=abc.ABCMeta):

    def __init__(self, *, parent=None):
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

    def __init__(self, fieldname, field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = fieldname
        self.field = field

    def display(self, column):
        if column == 0:
            return self.name
        elif column == 1:
            return type(self.field).__name__
        elif column == 2:
            return getattr(self.parent.hstruct, self.name)

    def icon(self):
        return get_icon()


class StructArrayNode(TreeNode):

    def __init__(self, fieldname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = fieldname
        for i, hstruct in enumerate(getattr(self.parent.hstruct, self.name)):
            StructNode('{} {}'.format(type(hstruct).__name__, i), hstruct, parent=self)

    def display(self, column):
        if column == 0:
            return self.name
        elif column == 1:
            return type(
                self.parent.hstruct.fields[self.name]).__name__

    def icon(self):
        return get_icon()


class StructNode(TreeNode):

    def __init__(self, name, hstruct, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.hstruct = hstruct
        if hstruct is not None:
            for fieldname, field in self.hstruct.fields.items():
                if isinstance(field, StructArray):
                    StructArrayNode(fieldname, parent=self)
                else:
                    FieldNode(fieldname, field, parent=self)

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
        StructNode('Header', htag.header, parent=self)
        StructNode('Data', getattr(htag, 'data'), parent=self)

    def display(self, column):
        if column == 0:
            return self.htag.name
        elif column == 1:
            return 'Tag'

    def icon(self):
        return get_icon()


class TagTypeNode(TreeNode):

    def __init__(self, tag_type, tags, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_type = tag_type
        x = list(sorted(tags(tag_type)))
        self.count = len(x)
        for tag in x:
            TagNode(tag, parent=self)

    def display(self, column):
        if column == 0:
            return '[{}] - {}'.format(
                self.tag_type,
                tag_names.get(self.tag_type, ''))
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
        StructNode('map_header', halomap.map_header, parent=self)
        StructNode('index_header', halomap.index_header, parent=self)
        tag_index = TagIndexNode(parent=self)
        for tag_type in sorted(self.halomap.tag_types):
            TagTypeNode(tag_type, self.halomap.tags, parent=tag_index)

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
