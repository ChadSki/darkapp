from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QTreeView, QListView, QFileSystemModel, QApplication)

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

def main(argv):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
         
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_())
