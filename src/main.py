import sys

from PyQt6.QtWidgets import QApplication

from controller.MainWindowController import MainWindowController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindowController()

    app.exec()