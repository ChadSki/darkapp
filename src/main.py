from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QTreeView, QListView, QFileSystemModel, QApplication)

from PyQt5.QtGui import QPalette as qp


class Main(QTreeView):
    def __init__(self):
        QTreeView.__init__(self)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        model = QFileSystemModel()
        model.setRootPath('C:\\')
        self.setModel(model)
        self.doubleClicked.connect(self.test)

    def test(self, signal):
        file_path = self.model().filePath(signal)
        print(file_path)


def build_palette():
    palette = QtGui.QPalette()
    foreground = QtCore.Qt.white
    accent = QtGui.QColor(53, 53, 53)
    background = QtGui.QColor(15, 15, 15)
    highlight = QtGui.QColor(142, 45, 197).lighter()
    highlight_foreground = QtCore.Qt.black
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
            (qp.HighlightedText, highlight_foreground)):
        palette.setColor(item, color)
    return palette


def main(argv):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(build_palette())
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_())
