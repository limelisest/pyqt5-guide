from ui import Ui_Keyboard
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class KeyBoard(QDialog):
    _key = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # 窗口初始化
        self.level = None
        self.ui = Ui_Keyboard.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowDoesNotAcceptFocus)
        # 按键绑定
        self.ui.button_num1.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num1.text()}'))
        self.ui.button_num2.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num2.text()}'))
        self.ui.button_num3.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num3.text()}'))
        self.ui.button_num4.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num4.text()}'))
        self.ui.button_num5.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num5.text()}'))
        self.ui.button_num6.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num6.text()}'))
        self.ui.button_num7.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num7.text()}'))
        self.ui.button_num8.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num8.text()}'))
        self.ui.button_num9.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num9.text()}'))
        self.ui.button_num0.clicked.connect(lambda: self._key.emit(f'{self.ui.button_num0.text()}'))
        self.ui.button_q.clicked.connect(lambda: self._key.emit(f'{self.ui.button_q.text()}'))
        self.ui.button_w.clicked.connect(lambda: self._key.emit(f'{self.ui.button_w.text()}'))
        self.ui.button_e.clicked.connect(lambda: self._key.emit(f'{self.ui.button_e.text()}'))
        self.ui.button_r.clicked.connect(lambda: self._key.emit(f'{self.ui.button_r.text()}'))
        self.ui.button_t.clicked.connect(lambda: self._key.emit(f'{self.ui.button_t.text()}'))
        self.ui.button_y.clicked.connect(lambda: self._key.emit(f'{self.ui.button_y.text()}'))
        self.ui.button_u.clicked.connect(lambda: self._key.emit(f'{self.ui.button_u.text()}'))
        self.ui.button_i.clicked.connect(lambda: self._key.emit(f'{self.ui.button_i.text()}'))
        self.ui.button_o.clicked.connect(lambda: self._key.emit(f'{self.ui.button_o.text()}'))
        self.ui.button_p.clicked.connect(lambda: self._key.emit(f'{self.ui.button_p.text()}'))

        self.ui.button_a.clicked.connect(lambda: self._key.emit(f'{self.ui.button_a.text()}'))
        self.ui.button_s.clicked.connect(lambda: self._key.emit(f'{self.ui.button_s.text()}'))
        self.ui.button_d.clicked.connect(lambda: self._key.emit(f'{self.ui.button_d.text()}'))
        self.ui.button_f.clicked.connect(lambda: self._key.emit(f'{self.ui.button_f.text()}'))
        self.ui.button_g.clicked.connect(lambda: self._key.emit(f'{self.ui.button_g.text()}'))
        self.ui.button_h.clicked.connect(lambda: self._key.emit(f'{self.ui.button_h.text()}'))
        self.ui.button_j.clicked.connect(lambda: self._key.emit(f'{self.ui.button_j.text()}'))
        self.ui.button_k.clicked.connect(lambda: self._key.emit(f'{self.ui.button_k.text()}'))
        self.ui.button_l.clicked.connect(lambda: self._key.emit(f'{self.ui.button_l.text()}'))

        self.ui.button_z.clicked.connect(lambda: self._key.emit(f'{self.ui.button_z.text()}'))
        self.ui.button_x.clicked.connect(lambda: self._key.emit(f'{self.ui.button_x.text()}'))
        self.ui.button_c.clicked.connect(lambda: self._key.emit(f'{self.ui.button_c.text()}'))
        self.ui.button_v.clicked.connect(lambda: self._key.emit(f'{self.ui.button_v.text()}'))
        self.ui.button_b.clicked.connect(lambda: self._key.emit(f'{self.ui.button_b.text()}'))
        self.ui.button_n.clicked.connect(lambda: self._key.emit(f'{self.ui.button_n.text()}'))
        self.ui.button_m.clicked.connect(lambda: self._key.emit(f'{self.ui.button_m.text()}'))

        self.ui.button_cap.clicked.connect(self.key_CAP)
        self.ui.button_enter.clicked.connect(lambda: self._key.emit('enter'))
        self.ui.button_back.clicked.connect(lambda: self._key.emit('back'))
        self.ui.button_left.clicked.connect(lambda: self._key.emit('left'))
        self.ui.button_right.clicked.connect(lambda: self._key.emit('right'))

    def key_CAP(self):
        if self.ui.button_cap.text() == "大写":
            self.ui.button_cap.setText("小写")
            self.ui.button_q.setText('Q')
            self.ui.button_w.setText('W')
            self.ui.button_e.setText('E')
            self.ui.button_r.setText('R')
            self.ui.button_t.setText('T')
            self.ui.button_y.setText('Y')
            self.ui.button_u.setText('U')
            self.ui.button_i.setText('I')
            self.ui.button_o.setText('O')
            self.ui.button_p.setText('P')

            self.ui.button_a.setText('A')
            self.ui.button_s.setText('S')
            self.ui.button_d.setText('D')
            self.ui.button_f.setText('F')
            self.ui.button_g.setText('G')
            self.ui.button_h.setText('H')
            self.ui.button_j.setText('J')
            self.ui.button_k.setText('K')
            self.ui.button_l.setText('L')

            self.ui.button_z.setText('Z')
            self.ui.button_x.setText('X')
            self.ui.button_c.setText('C')
            self.ui.button_v.setText('V')
            self.ui.button_b.setText('B')
            self.ui.button_n.setText('N')
            self.ui.button_m.setText('M')
        else:
            self.ui.button_cap.setText("大写")
            self.ui.button_q.setText('q')
            self.ui.button_w.setText('w')
            self.ui.button_e.setText('e')
            self.ui.button_r.setText('r')
            self.ui.button_t.setText('t')
            self.ui.button_y.setText('y')
            self.ui.button_u.setText('u')
            self.ui.button_i.setText('i')
            self.ui.button_o.setText('o')
            self.ui.button_p.setText('p')

            self.ui.button_a.setText('a')
            self.ui.button_s.setText('s')
            self.ui.button_d.setText('d')
            self.ui.button_f.setText('f')
            self.ui.button_g.setText('g')
            self.ui.button_h.setText('h')
            self.ui.button_j.setText('j')
            self.ui.button_k.setText('k')
            self.ui.button_l.setText('l')

            self.ui.button_z.setText('z')
            self.ui.button_x.setText('x')
            self.ui.button_c.setText('c')
            self.ui.button_v.setText('v')
            self.ui.button_b.setText('b')
            self.ui.button_n.setText('n')
            self.ui.button_m.setText('m')
        pass

    @property
    def key(self):
        return self._key
