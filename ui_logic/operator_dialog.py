import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui import Ui_Operator

import event.device
import event.sql


class OperatorDialog(QDialog):
    _signal = pyqtSignal(list)
    _user = '?'

    def __init__(self):
        super().__init__()
        # 成员初始化
        self.sql = event.sql.MySQl()
        # 窗口初始化
        self.level = None
        self.ui = Ui_Operator.Ui_OperatorDialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.showFullScreen()
        # 组件初始化
        self.ui.label_uuid.setText(f'UUID:{event.device.get_uuid()}')
        self.signal.connect(self.set_user)
        # 事件绑定
        self.ui.button_close.clicked.connect(self.button_close)
        self.ui.button_quit.clicked.connect(self.button_quit)
        self.ui.button_reset_UUID.clicked.connect(self.button_reset_UUID)
        self.ui.button_change_password.clicked.connect(self.button_change_password)

    def set_user(self, _list):
        self._user = _list[0]
        self.level = _list[1]
        self.ui.label_op_user.setText(f'账号：{self._user}')
        self.ui.label_op_level.setText(f'权限等级：{self.level}')

    def button_change_password(self):
        text_old_password = self.ui.line_old_password.text()
        text_new_password_1 = self.ui.lineEdit_new_password_1.text()
        text_new_password_2 = self.ui.lineEdit_new_password_2.text()

        if not text_old_password or not text_new_password_1 or not text_new_password_2:  # 非空检测
            self.ui.button_change_password.setText("密码不能为空")

        elif not text_new_password_1 == text_new_password_2:
            self.ui.button_change_password.setText("两次密码不一致")

        elif text_old_password == text_new_password_2:
            self.ui.button_change_password.setText("新密码不能与原密码一致")

        elif self.sql.change_operator(self._user, text_old_password, text_new_password_2):
            self.ui.button_change_password.setText("密码修改成功")
            self.ui.groupBox_3.setEnabled(False)

        else:
            self.ui.button_change_password.setText("原密码不匹配")

    def button_reset_UUID(self):
        event.device.reset_uuid()
        self.ui.button_reset_UUID.setText("重置UUID成功")
        self.ui.label_uuid.setText(f'UUID:{event.device.get_uuid()}')

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
