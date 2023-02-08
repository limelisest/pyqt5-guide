from paho.mqtt import client as mqtt_client
from PyQt5.QtCore import *
from event import device

_ip = '120.79.71.233'
_port = 1883


class MQTTThread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ip = _ip
        self.port = _port
        self.uuid = device.get_uuid()
        self.client = mqtt_client.Client(f'{self.uuid}')
        self.init_client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.disconnect()

    def init_client(self):
        """
        初始化MQTT客户端，包括连接部分
        :return:无
        """

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                self.send_message('qt', f'connect topic:{self.uuid}')
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client.on_connect = on_connect
        self.client.connect(self.ip, self.port)

    def send_message(self, _topic, msg):
        result = self.client.publish(_topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{_topic}`")
            return 0
        else:
            print(f"Failed to send message to topic {_topic}")
            return -1

    def get_message(self, _topic):
        def on_message(client, userdata, msg):
            print(f'Topic:{msg.topic}\nMessage:\n{msg.payload.decode()}')
            self._signal.emit(msg.payload.decode())

        self.client.subscribe(_topic)
        self.client.on_message = on_message

    def run(self):
        self.get_message(f'{self.uuid}')
        self.client.loop_forever()

    @property
    def signal(self):
        return self._signal
