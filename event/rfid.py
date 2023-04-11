import re
import time

import mfrc522
from PyQt5.QtCore import QThread, pyqtSignal
from RPi import GPIO


class RFIDThread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self):
        super(RFIDThread, self).__init__()
        self.reader = mfrc522.MFRC522()

    @property
    def signal(self):
        return self._signal

    def run(self):
        while True:
            # Scan for cards
            (status, TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
            # Get the UID of the card
            (status, uid) = self.reader.MFRC522_Anticoll()
            # If we have the UID, continue
            if status == self.reader.MI_OK and uid != '':
                val1 = hex(uid[0])[2:].upper()
                val2 = hex(uid[1])[2:].upper()
                val3 = hex(uid[2])[2:].upper()
                val4 = hex(uid[3])[2:].upper()
                # Print UID
                # print(f"UID: {val1}{val2}{val3}{val4}")
                self._signal.emit(f'{val1}{val2}{val3}{val4}')
                GPIO.cleanup()
                time.sleep(2)
