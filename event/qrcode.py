from PyQt5.QtCore import *
import time
import cv2
import numpy as np
from pyzbar import pyzbar as pyzbar

camera_id = 0


# 扫描线程
class QRCodeThread(QThread):
    """
    扫描线程，线程信号：signal()
    """
    _signal = pyqtSignal(list)

    def __init__(self):
        super(QRCodeThread, self).__init__()

    def run(self):

        camera = cv2.VideoCapture(camera_id)
        print(camera)
        while True:
            ret, frame = camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)  # 定义一个核
            dst = cv2.filter2D(gray, -1, kernel=kernel)
            barcodes = pyzbar.decode(dst)
            for barcode in barcodes:
                if barcode != '':
                    barcode_data = barcode.data.decode("UTF8")
                    barcode_type = barcode.type
                    print(f"[INFO] Found {barcode_type} barcode: {barcode_data}")
                    # item = Item(itemid=f"{barcode_data}",
                    #             name=f"{barcode_data}|{barcode_type}",
                    #             price=648,
                    #             num=1)
                    if barcode_type == "QRCODE" or barcode_type == "EAN13":
                        self._signal.emit([barcode_type, barcode_data])
                    camera.release()
                    camera = cv2.VideoCapture(camera_id)
                    time.sleep(2)

    @property
    def signal(self):
        return self._signal
