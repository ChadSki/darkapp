# Note: This script has been baked into darkapp.exe and is included only for
# reference. Changes should go into main.py, or you can recompile darkapp.

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QTreeView, QListView, QFileSystemModel, QApplication)
import sys

if getattr(sys, 'frozen', False):
    # running in a bundle, do path muckery
    here = os.path.dirname(sys.executable)
    sys.path.insert(1, here)

import main
main.main(sys.argv)
