import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui import Ui_Operator, Ui_Keyboard

import event.device
import event.sql
from ui_logic import KeyBoard


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
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(0, 0)
        # 组件初始化
        self.ui.label_uuid.setText(f'UUID:{event.device.get_uuid()}')
        self.signal.connect(self.set_user)
        # 事件绑定
        self.ui.button_close.clicked.connect(self.button_close)
        self.ui.button_quit.clicked.connect(self.button_quit)
        self.ui.button_reset_UUID.clicked.connect(self.button_reset_UUID)
        self.ui.button_change_password.clicked.connect(self.button_change_password)
        # 键盘事件侦听
        widget_ui = Ui_Keyboard.Ui_KeyBoardWidget()
        widget_ui.setupUi(self.ui.widget_keyboard)
        keyboard = KeyBoard.KeyBoard()
        keyboard.key.connect(self.on_keyboard)
        keyboard.init_key(widget_ui)

    def on_keyboard(self, msg):
        """
        收到键盘信号时候的处理
        :param msg: str
        :return:
        """
        if msg == "enter":
            if self.ui.line_old_password.hasFocus():
                self.ui.lineEdit_new_password_1.setFocus()
            elif self.ui.lineEdit_new_password_1.hasFocus():
                self.ui.lineEdit_new_password_2.setFocus()
            elif self.ui.lineEdit_new_password_2.hasFocus():
                self.ui.button_change_password.click()

        elif msg == "back":
            if self.ui.line_old_password.hasFocus():
                self.ui.line_old_password.setText(
                    f'{self.ui.line_old_password.text()[:len(self.ui.line_old_password.text()) - 1]}')
            elif self.ui.lineEdit_new_password_1.hasFocus():
                self.ui.lineEdit_new_password_1.setText(
                    f'{self.ui.lineEdit_new_password_1.text()[:len(self.ui.lineEdit_new_password_1.text()) - 1]}')
            elif self.ui.lineEdit_new_password_2.hasFocus():
                self.ui.lineEdit_new_password_2.setText(
                    f'{self.ui.lineEdit_new_password_2.text()[:len(self.ui.lineEdit_new_password_2.text()) - 1]}')

        elif msg == "left":
            if self.ui.line_old_password.hasFocus():
                self.ui.line_old_password.cursorBackward(False, 1)
            elif self.ui.lineEdit_new_password_1.hasFocus():
                self.ui.lineEdit_new_password_1.cursorBackward(False, 1)
            elif self.ui.lineEdit_new_password_2.hasFocus():
                self.ui.lineEdit_new_password_2.cursorBackward(False, 1)

        elif msg == "right":
            if self.ui.line_old_password.hasFocus():
                self.ui.line_old_password.cursorForward(False, 1)
            elif self.ui.lineEdit_new_password_1.hasFocus():
                self.ui.lineEdit_new_password_1.cursorForward(False, 1)
            elif self.ui.lineEdit_new_password_2.hasFocus():
                self.ui.lineEdit_new_password_2.cursorForward(False, 1)

        elif self.ui.line_old_password.hasFocus():
            self.ui.line_old_password.setText(f'{self.ui.line_old_password.text()}{msg}')
        elif self.ui.lineEdit_new_password_1.hasFocus():
            self.ui.lineEdit_new_password_1.setText(f'{self.ui.lineEdit_new_password_1.text()}{msg}')
        elif self.ui.lineEdit_new_password_2.hasFocus():
            self.ui.lineEdit_new_password_2.setText(f'{self.ui.lineEdit_new_password_2.text()}{msg}')

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
