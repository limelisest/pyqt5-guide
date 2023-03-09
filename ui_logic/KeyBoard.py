from ui import Ui_Keyboard
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets


class KeyBoard(QWidget):
    _key = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # 窗口初始化
        self.level = None
        self.ui = Ui_Keyboard.Ui_KeyBoardWidget()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.NonModal)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowDoesNotAcceptFocus)
        self.init_key(self.ui)

    def init_key(self, ui):
        def key_CAP():
            if ui.button_cap.text() == "大写":
                ui.button_cap.setText("小写")
                ui.button_q.setText('Q')
                ui.button_w.setText('W')
                ui.button_e.setText('E')
                ui.button_r.setText('R')
                ui.button_t.setText('T')
                ui.button_y.setText('Y')
                ui.button_u.setText('U')
                ui.button_i.setText('I')
                ui.button_o.setText('O')
                ui.button_p.setText('P')

                ui.button_a.setText('A')
                ui.button_s.setText('S')
                ui.button_d.setText('D')
                ui.button_f.setText('F')
                ui.button_g.setText('G')
                ui.button_h.setText('H')
                ui.button_j.setText('J')
                ui.button_k.setText('K')
                ui.button_l.setText('L')

                ui.button_z.setText('Z')
                ui.button_x.setText('X')
                ui.button_c.setText('C')
                ui.button_v.setText('V')
                ui.button_b.setText('B')
                ui.button_n.setText('N')
                ui.button_m.setText('M')
            else:
                ui.button_cap.setText("大写")
                ui.button_q.setText('q')
                ui.button_w.setText('w')
                ui.button_e.setText('e')
                ui.button_r.setText('r')
                ui.button_t.setText('t')
                ui.button_y.setText('y')
                ui.button_u.setText('u')
                ui.button_i.setText('i')
                ui.button_o.setText('o')
                ui.button_p.setText('p')

                ui.button_a.setText('a')
                ui.button_s.setText('s')
                ui.button_d.setText('d')
                ui.button_f.setText('f')
                ui.button_g.setText('g')
                ui.button_h.setText('h')
                ui.button_j.setText('j')
                ui.button_k.setText('k')
                ui.button_l.setText('l')

                ui.button_z.setText('z')
                ui.button_x.setText('x')
                ui.button_c.setText('c')
                ui.button_v.setText('v')
                ui.button_b.setText('b')
                ui.button_n.setText('n')
                ui.button_m.setText('m')

        # 按键绑定
        ui.button_num1.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num1.text()}'))
        ui.button_num2.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num2.text()}'))
        ui.button_num3.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num3.text()}'))
        ui.button_num4.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num4.text()}'))
        ui.button_num5.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num5.text()}'))
        ui.button_num6.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num6.text()}'))
        ui.button_num7.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num7.text()}'))
        ui.button_num8.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num8.text()}'))
        ui.button_num9.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num9.text()}'))
        ui.button_num0.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num0.text()}'))

        ui.button_q.clicked.connect(lambda: self._key.emit(f'{self.ui.button_q.text()}'))
        ui.button_w.clicked.connect(lambda: self._key.emit(f'{self.ui.button_w.text()}'))
        ui.button_e.clicked.connect(lambda: self._key.emit(f'{self.ui.button_e.text()}'))
        ui.button_r.clicked.connect(lambda: self._key.emit(f'{self.ui.button_r.text()}'))
        ui.button_t.clicked.connect(lambda: self._key.emit(f'{self.ui.button_t.text()}'))
        ui.button_y.clicked.connect(lambda: self._key.emit(f'{self.ui.button_y.text()}'))
        ui.button_u.clicked.connect(lambda: self._key.emit(f'{self.ui.button_u.text()}'))
        ui.button_i.clicked.connect(lambda: self._key.emit(f'{self.ui.button_i.text()}'))
        ui.button_o.clicked.connect(lambda: self._key.emit(f'{self.ui.button_o.text()}'))
        ui.button_p.clicked.connect(lambda: self._key.emit(f'{self.ui.button_p.text()}'))

        ui.button_a.clicked.connect(lambda: self._key.emit(f'{self.ui.button_a.text()}'))
        ui.button_s.clicked.connect(lambda: self._key.emit(f'{self.ui.button_s.text()}'))
        ui.button_d.clicked.connect(lambda: self._key.emit(f'{self.ui.button_d.text()}'))
        ui.button_f.clicked.connect(lambda: self._key.emit(f'{self.ui.button_f.text()}'))
        ui.button_g.clicked.connect(lambda: self._key.emit(f'{self.ui.button_g.text()}'))
        ui.button_h.clicked.connect(lambda: self._key.emit(f'{self.ui.button_h.text()}'))
        ui.button_j.clicked.connect(lambda: self._key.emit(f'{self.ui.button_j.text()}'))
        ui.button_k.clicked.connect(lambda: self._key.emit(f'{self.ui.button_k.text()}'))
        ui.button_l.clicked.connect(lambda: self._key.emit(f'{self.ui.button_l.text()}'))

        ui.button_z.clicked.connect(lambda: self._key.emit(f'{self.ui.button_z.text()}'))
        ui.button_x.clicked.connect(lambda: self._key.emit(f'{self.ui.button_x.text()}'))
        ui.button_c.clicked.connect(lambda: self._key.emit(f'{self.ui.button_c.text()}'))
        ui.button_v.clicked.connect(lambda: self._key.emit(f'{self.ui.button_v.text()}'))
        ui.button_b.clicked.connect(lambda: self._key.emit(f'{self.ui.button_b.text()}'))
        ui.button_n.clicked.connect(lambda: self._key.emit(f'{self.ui.button_n.text()}'))
        ui.button_m.clicked.connect(lambda: self._key.emit(f'{self.ui.button_m.text()}'))

        ui.button_cap.clicked.connect(key_CAP)
        ui.button_enter.clicked.connect(lambda: self._key.emit('enter'))
        ui.button_back.clicked.connect(lambda: self._key.emit('back'))
        ui.button_left.clicked.connect(lambda: self._key.emit('left'))
        ui.button_right.clicked.connect(lambda: self._key.emit('right'))

    @property
    def key(self):
        return self._key
