import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QTreeView, QApplication)

from PyQt5.QtGui import QPalette as qp

from gui import HaloModel


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


class MainTree(QTreeView):
    def __init__(self):
        QTreeView.__init__(self)
        self.setModel(HaloModel(
            "C:\\Program Files (x86)\\Microsoft Games\\Halo\\MAPS\\bloodgulch.map"))
        self.setWindowTitle('Darkapp')
        self.resize(900, 800)
        self.setColumnWidth(0, 550)
        self.setColumnWidth(1, 100)


class MainApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyle('Fusion')
        self.setPalette(build_palette())


def main(argv):
    app = MainApplication(argv)
    tree = MainTree()
    tree.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
