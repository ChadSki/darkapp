import os
import sys
from PyQt5 import QtGui

icon_cache = {}


def get_icon(name='open_folder'):
    global icon_cache
    if name not in icon_cache:
        path = os.path.join(
            os.path.dirname(sys.modules[__name__].__file__),
            '{}.svg'.format(name))
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(
            QtGui.QPixmap(path),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        icon_cache[name] = new_icon
    return icon_cache[name]
