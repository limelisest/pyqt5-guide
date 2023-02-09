import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui import Ui_Operator

import main


class OperatorDialog(QDialog):
    _signal = pyqtSignal(list)
    _user = '?'

    def __init__(self):
        super().__init__()
        # 窗口初始化
        self.level = None
        self.ui = Ui_Operator.Ui_OperatorDialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        # self.showFullScreen()

        # 事件绑定
        self.ui.button_close.clicked.connect(self.button_close)
        self.ui.button_quit.clicked.connect(self.button_quit)
        # self.ui.button_reset_UUID.clicked.connect()
        # self.ui.button_change_password.clicked.connect()
        self.signal.connect(self.set_user)

    def set_user(self, _list):
        self._user = _list[0]
        self.level = _list[1]
        self.ui.label_op_user.setText(f'账号：{self._user}')
        self.ui.label_op_level.setText(f'权限等级：{self.level}')

    def button_close(self):
        self.close()

    def button_quit(self):
        self.signal.emit("quit")
        self.close()

    def closeEvent(self, event):
        print("op窗口被关闭")

    @property
    def signal(self):
        return self._signal
