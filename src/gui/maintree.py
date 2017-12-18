from PyQt5.QtWidgets import QTreeView

from .halomodel import HaloModel


class MainTree(QTreeView):
    def __init__(self):
        QTreeView.__init__(self)
        self.setModel(HaloModel(
            "C:\\Program Files (x86)\\Microsoft Games\\Halo\\MAPS\\bloodgulch.map"))
        self.setWindowTitle('Darkapp')
        self.resize(900, 800)
        self.setColumnWidth(0, 550)
        self.setColumnWidth(1, 100)
