import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from event.sql import MySQl
from ui import QRcode
from event.mqtt import MQTTThread, device
import qrcode


class QRcode_dialog(QDialog):
    _signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        # 变量初始化
        self.sql = MySQl()
        # 窗口初始化
        self.ui = QRcode.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(0, 0)
        # 组件初始化
        self.init_qrcode()
        self.ui.label_qr_code.setScaledContents(True)
        # 按钮绑定
        self.ui.button_cancel.clicked.connect(self.cancel_button)
        # 多线程
        self.mqtt_thread = MQTTThread()
        self.mqtt_thread.signal.connect(self.mqtt_thread_call_back)
        self.mqtt_thread.start()

    def mqtt_thread_call_back(self, msg):
        """
        MQTT多线程回调函数
        :param msg:str
        :return:
        """
        try:
            guide_list = []
            json_data = json.loads(msg)
            user_id = ""
            guide_id_dict = {}
            if json_data['user']:
                user_id = json_data['user']
            if json_data['list']:
                guide_id_dict = json_data['list']
            self.ui.label_error.setText(f'user:{user_id}\nlist:{guide_id_dict}')

            for item_id in guide_id_dict:
                item_num = guide_id_dict[item_id]
                item = self.sql.get_item(item_id)
                if item:
                    item.set_num(item_num)
                    guide_list.append(item)

            self._signal.emit(guide_list)
            self.close()
        except json.JSONDecodeError:
            self.ui.label_error.setText(f'mqtt:{msg}\n数据错误，请重新扫码')

    def cancel_button(self):
        """
        取消按钮
        :return:
        """
        self.close()

    def closeEvent(self, event):
        print("关闭了窗口")
        self.mqtt_thread.terminate()
        self.mqtt_thread.wait()

    def init_qrcode(self):
        """
        生成一个专属于这个设备的topic,并使用二维码显示
        :return:
        """
        qr = qrcode.QRCode(
            version=1,  # 二维码格子的矩阵大小 1-40（1：21*21）
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # 二维码错误允许率
            box_size=10,  # 每个小格子包含的像素数量
            border=2,  # 二维码到图片边框的小格子数
        )  # 设置图片格式

        # 输入数据
        qr.add_data(device.get_uuid())
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        file_name = './device/qrcode.png'
        img.save(file_name)  # 生成图片
        self.ui.label_qr_code.setPixmap(QPixmap(file_name))

    @property
    def signal(self):
        return self._signal
