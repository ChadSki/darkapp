import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QTreeView, QListView, QFileSystemModel, QApplication)
import sys

if getattr( sys, 'frozen', False ) :
    # running in a bundle, do path muckery
    print(sys.path)
    here = os.path.dirname(sys.executable)
    sys.path.insert(1, here)
    print(sys.path)

import main
main.main(sys.argv)
