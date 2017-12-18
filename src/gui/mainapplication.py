from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette as qp

from .maintree import MainTree


def build_palette():
    palette = QtGui.QPalette()
    foreground = QtCore.Qt.white
    accent = QtGui.QColor(53, 53, 53)
    background = QtGui.QColor(15, 15, 15)
    highlight = QtGui.QColor(202, 81, 0)
    for item, color in (
            (qp.Window, accent),
            (qp.WindowText, foreground),
            (qp.Base, background),
            (qp.AlternateBase, accent),
            (qp.ToolTipBase, foreground),
            (qp.ToolTipText, foreground),
            (qp.Text, foreground),
            (qp.Button, accent),
            (qp.ButtonText, foreground),
            (qp.BrightText, QtCore.Qt.red),
            (qp.Highlight, highlight),
            (qp.HighlightedText, foreground)):
        palette.setColor(item, color)
    palette.setColor(qp.Disabled, qp.Light, QtCore.Qt.transparent)
    palette.setColor(qp.Disabled, qp.Text, accent.lighter())
    return palette


class MainApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyle('Fusion')
        self.setPalette(build_palette())
        self.tree = MainTree()
        self.tree.show()
