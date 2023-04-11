import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import *

from event import device
from ui import Ui_main, Ui_Keyboard
from ui_logic import QRcode_dialog, Operator, KeyBoard
import event.sql
import event.guide
import event.item
import event.qrcode
import event.device
import event.mqtt


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        # 类初始化
        self.guide = event.guide.Guide()
        self.buy_list = event.item.Buy_Item_List()
        self.sql = event.sql.MySQl()
        # 设置窗口
        self.ui = Ui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(0, 0)
        self.init_map()
        # 事件绑定
        self.ui.button_debug_2.clicked.connect(self.debug_2)
        self.ui.button_debug_3.clicked.connect(self.debug_3)
        self.ui.button_add_guide_list.clicked.connect(self.open_qrcode_dialog)
        self.ui.button_enter_operator.clicked.connect(self.enter_operator)
        self.ui.list_guide.itemClicked.connect(self.list_guide_itemClicked)
        self.ui.button_settlement.clicked.connect(self.settlement)
        # 多线程
        self.qrcode_thread = event.qrcode.QRCodeThread()
        self.qrcode_thread.signal.connect(self.qrcode_thread_callback)
        self.qrcode_thread.start()
        # 键盘事件侦听
        widget_ui = Ui_Keyboard.Ui_KeyBoardWidget()
        widget_ui.setupUi(self.ui.widget_keyboard)
        keyboard = KeyBoard.KeyBoard()
        keyboard.key.connect(self.on_keyboard)
        keyboard.init_key(widget_ui)

    def settlement(self):
        """
        结算
        :return:
        """
        if device.user_id == '':
            QMessageBox.question(self, '请登录', '请先导入购物清单', QMessageBox.Yes)
            return 0
        a = QMessageBox.question(self, '结算', '你确定要结算吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if a == QMessageBox.Yes:
            self.sql.update_order(self.buy_list.list)
            self.buy_list.list.clear()
            self.guide.get_list().clear()
            self.ui.list_buy.clear()
            self.ui.list_guide.clear()
            device.user_id = ''
            QMessageBox.question(self, '结算', '结算成功', QMessageBox.Yes)

    def list_guide_itemClicked(self):
        """
        在地图上高亮选中的地点
        :return:
        """
        count = 0
        for item in self.guide.get_list():
            count += 1
            area_x, area_y = item.area
            self.map_draw_point(area_x, area_y, f"{count}", 3)

        index = self.ui.list_guide.currentRow()
        x, y = self.guide.get_list()[index].area
        self.map_draw_point(x, y, f'{index + 1}', 2, 0)

    def init_map(self):
        """
        初始化导购地图
        :return:
        """
        table_w = self.ui.tableWidget.geometry().width()
        table_h = self.ui.tableWidget.geometry().height()
        box_w = int(table_w / 16) - 1
        box_h = int(table_h / 16) - 1
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(box_w)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(box_h)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setEnabled(False)
        # 绘制地图
        for y in range(16):
            for x in range(16):
                item = QTableWidgetItem()
                if self.guide.map[x][y] == 0:
                    item.setBackground(QColor(0, 0, 0, 200))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.ui.tableWidget.setItem(x, y, item)

    def map_draw_points_on_guide(self):
        # 绘制地图
        for y in range(16):
            for x in range(16):
                item = QTableWidgetItem()
                if self.guide.map[x][y] == 0:
                    item.setBackground(QColor(0, 0, 0, 200))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.ui.tableWidget.setItem(x, y, item)
        count = 0
        for item in self.guide.get_list():
            count += 1
            area_x, area_y = item.area
            self.map_draw_point(area_x, area_y, f"{count}", 3)

    def map_draw_point(self, x: int, y: int, text='', backgroundColor=1, textColor=0):
        """
        从地图上绘制一个格子。颜色：0:黑色, 1:白色, 2:紫色, 3:灰色 4:黄色
        """
        color_black = QColor(0, 0, 0, 200)
        color_white = QColor(255, 255, 255, 255)
        color_purple = QColor(222, 200, 249, 255)
        color_gery = QColor(125, 125, 125)
        color_yellow = QColor(0, 255, 255, 125)
        table_item = QTableWidgetItem()

        if backgroundColor == 0:
            table_item.setBackground(color_black)
        elif backgroundColor == 1:
            table_item.setBackground(color_white)
        elif backgroundColor == 2:
            table_item.setBackground(color_purple)
        elif backgroundColor == 3:
            table_item.setBackground(color_gery)
        elif backgroundColor == 4:
            table_item.setBackground(color_yellow)

        if textColor == 0:
            table_item.setForeground(color_black)
        elif textColor == 1:
            table_item.setForeground(color_white)
        elif textColor == 2:
            table_item.setForeground(color_purple)
        elif textColor == 3:
            table_item.setForeground(color_gery)
        elif textColor == 4:
            table_item.setForeground(color_yellow)

        table_item.setText(text)
        table_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        table_item.setTextAlignment(Qt.AlignCenter)
        self.ui.tableWidget.setItem(y, x, table_item)

    def on_keyboard(self, msg):
        """
        收到键盘信号时候的处理
        :param msg: str
        :return:
        """
        if msg == "enter":
            if self.ui.line_user.hasFocus():
                self.ui.line_password.setFocus()
            elif self.ui.line_password.hasFocus():
                self.ui.button_enter_operator.click()
        elif msg == "back":
            if self.ui.line_user.hasFocus():
                self.ui.line_user.setText(f'{self.ui.line_user.text()[:len(self.ui.line_user.text()) - 1]}')
            elif self.ui.line_password.hasFocus():
                self.ui.line_password.setText(f'{self.ui.line_password.text()[:len(self.ui.line_password.text()) - 1]}')
        elif msg == "left":
            if self.ui.line_user.hasFocus():
                self.ui.line_user.cursorBackward(False, 1)
            elif self.ui.line_password.hasFocus():
                self.ui.line_password.cursorBackward(False, 1)
        elif msg == "right":
            if self.ui.line_user.hasFocus():
                self.ui.line_user.cursorForward(False, 1)
            elif self.ui.line_password.hasFocus():
                self.ui.line_password.cursorForward(False, 1)
        elif self.ui.line_user.hasFocus():
            self.ui.line_user.setText(f'{self.ui.line_user.text()}{msg}')
        elif self.ui.line_password.hasFocus():
            self.ui.line_password.setText(f'{self.ui.line_password.text()}{msg}')

    def enter_operator(self):
        def op_quit(msg):
            if msg == "quit":
                self.close()

        op_user = self.ui.line_user.text()
        op_password = self.ui.line_password.text()
        level = self.sql.check_operator(op_user, op_password)
        if level:
            op_dialog = Operator.OperatorDialog()
            op_dialog.signal.emit([op_user, level])  # 发送数据
            op_dialog.signal.connect(op_quit)  # 接收数据
            op_dialog.exec_()
        else:
            self.ui.label_op_error.setText(f"账号：{op_user}密码错误或者不存在")

    # 识别线程callback
    def qrcode_thread_callback(self, data):
        """
        扫描线程收到信号后的处理
        :param data:[type,data]
        :return:
        """
        qr_type, qr_data = data
        print(f"f[QRCODE SCAN]type:<{qr_type}>,data:<{qr_data}>")
        self.buy_list_add_item(qr_data, qr_type)

    def open_qrcode_dialog(self):
        # 添加购买列表
        def guide_list_refresh(guide_list):
            """
            读取预购的列表从MQTT读取
            :return:
            """
            self.init_map()
            self.guide.set_list(guide_list)
            self.guide.list.sorted()
            if self.guide.get_list():
                for item in self.guide.get_list():
                    self.guide_list_add_ui(item)

                self.map_draw_points_on_guide()
                self.ui.label_guide_item_name.setText(f'{self.guide.get_list()[0].name}')
                self.ui.label_guide_item_area.setText(f'{self.guide.get_list()[0].area}')
            print(f"qrcode_dialog return:{guide_list}")

        qrcode_dialog = QRcode_dialog.QRcode_dialog()
        qrcode_dialog.signal.connect(guide_list_refresh)
        qrcode_dialog.exec_()

    def debug_2(self):
        if self.guide.get_list():
            item_id = self.guide.get_list()[0].id
            self.buy_list_add_item(item_id)

    def debug_3(self):
        for i in range(3):
            self.buy_list_add_item(i + 1)

    def buy_list_add_item(self, _id, _type="id"):
        """
        从结算列表里添加一个item
        :param _id: str
        :param _type: id类型：id、bar_id、qr_id、rf_id
        :return:
        """

        item = self.sql.get_item(_id, _type)
        if item:
            self.buy_list.add_item(item)
            self.ui.label_price.setText(f'{round(item.price, 2)} 元')
            self.ui.label_title.setText(f'{item.name}')
            self.ui.tabWidget.setCurrentIndex(1)
            # 判断添加的物品是否在导购列表里
            if self.guide.list.in_list(item.id):
                self.guide.list.reduce_item_from_id(item.id, item.num)
                self.map_draw_points_on_guide()
            self.buy_list_refresh()
            self.guide_list_refresh()
            self.ui.list_buy.scrollToBottom()

    def buy_list_reduce_item(self, itemid):
        """
        通过itemid减少一个物品，当为0时删除
        :param itemid:
        :return:
        """
        self.buy_list.reduce_item_from_id(itemid)
        self.buy_list_refresh()

    # 刷新预购列表
    def guide_list_refresh(self):
        self.ui.list_guide.clear()
        if self.guide.get_list():
            for item in self.guide.get_list():
                self.guide_list_add_ui(item)
            self.ui.label_guide_item_name.setText(f'{self.guide.get_list()[0].name}')
            self.ui.label_guide_item_area.setText(f'{self.guide.get_list()[0].area}')

    # 刷新购买列表
    def buy_list_refresh(self):
        """
        刷新结算列表
        :return:
        """
        self.ui.list_buy.clear()
        # 从字典读取所有数据刷新到列表GUI
        # 读取已购买的列表
        for item_id in self.buy_list.list.keys():
            item = self.buy_list.list[item_id]
            self.ui.label_all_price.setText(f'{self.buy_list.all_price} 元')
            self.buy_list_add_ui(item)
        if self.buy_list.all_price == 0:
            self.ui.label_all_price.setText(f'0 元')

    # 添加列表
    def buy_list_add_ui(self, item: event.item.Item):
        """
        通过自定义布局往结算列表添加一个项目
        该布局包含三个标签和一个按钮，数据内容:
        map_name = item.name
        map_price = item.price
        map_num = item.num
        :param item:
        :return:
        """
        itemid = item.id
        name = item.name
        price = item.price
        num = item.num
        # item 布局
        item = QListWidgetItem()
        item.setSizeHint(QSize(350, 80))
        wight_1 = QWidget()
        wight_2 = QWidget()
        layout_1 = QHBoxLayout()
        layout_2 = QVBoxLayout()

        map_name = QLabel(f'{name}')
        map_price = QLabel(f'{round(price, 2)} 元')
        map_num = QLabel(f"X {num}")
        map_num.setMaximumWidth(60)

        layout_2.addWidget(map_name)
        layout_2.addWidget(map_price)

        map_button = QPushButton()
        map_button.setText("不要了")
        map_button.setMaximumWidth(60)
        map_button.setMinimumHeight(60)

        def del_button():
            self.buy_list_reduce_item(itemid)

        map_button.clicked.connect(del_button)

        layout_1.addWidget(wight_2)
        layout_1.addWidget(map_num)
        layout_1.addWidget(map_button)

        wight_2.setLayout(layout_2)
        wight_1.setLayout(layout_1)  # 布局给layout_1

        self.ui.list_buy.addItem(item)
        self.ui.list_buy.setItemWidget(item, wight_1)  # 将布局应用给item

    def guide_list_add_ui(self, item: event.item.Item):
        """
        通过自定义布局往导购列表添加一个项目
        map_name = QLabel(f'{name}')
        map_area = QLabel(f'[{area_x},{area_y}] ')
        map_num = QLabel(f"X {num}")
        :param item:
        :return:
        """
        name = item.name
        area_x, area_y = item.area
        num = item.num

        # item 布局
        item = QListWidgetItem()
        item.setSizeHint(QSize(300, 80))
        wight_1 = QWidget()
        wight_2 = QWidget()
        layout_1 = QHBoxLayout()
        layout_2 = QVBoxLayout()

        map_name = QLabel(f'{name}')
        map_area = QLabel(f'[{area_x},{area_y}] ')
        map_num = QLabel(f"X {num}")
        map_num.setMaximumWidth(60)

        layout_2.addWidget(map_name)
        layout_2.addWidget(map_area)

        layout_1.addWidget(wight_2)
        layout_1.addWidget(map_num)

        wight_2.setLayout(layout_2)
        wight_1.setLayout(layout_1)  # 布局给layout_1

        self.ui.list_guide.addItem(item)
        self.ui.list_guide.setItemWidget(item, wight_1)  # 将布局应用给item
