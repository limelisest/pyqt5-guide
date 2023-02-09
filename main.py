# 导入要用到的类型
from PyQt5.QtWidgets import *
import sys
from ui_logic import my_window
if __name__ == '__main__':
    # 先实例化 app 对象
    app = QApplication(sys.argv)
    # 再实例化窗口类对象
    MainWindows = my_window.MyWindow()
    # 显示窗口
    MainWindows.show()
    # 启动消息循环
    sys.exit(app.exec_())
