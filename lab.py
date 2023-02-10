import sys
from PyQt5.QtWidgets import QApplication, QWidget
from ctypes import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 50
        self.top = 50
        self.width = 1200
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()


if __name__ == '__main__':
    FindWindow = windll.user32.FindWindowW
    SetParent = windll.user32.SetParent
    SetWindowPos = windll.user32.SetWindowPos
    # 打开老罗记事本，然后运行代码
    notepad_handle = FindWindow(0, "老罗笔记人工智能文字处理软件 Rogabet Notepad")
    app = QApplication(sys.argv)
    ex = App()
    SetParent(notepad_handle, int(ex.winId()))
    SetWindowPos(notepad_handle, 0, 100, 100, 400, 600, 0)
    sys.exit(app.exec_())
