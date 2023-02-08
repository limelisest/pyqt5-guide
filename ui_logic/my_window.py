import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ui import Ui_main
from ui_logic import QRcode_dialog
from event.item import Item, Buy_Item_List
from event.guide import Guide
from event.qrcode import QRCodeThread


class MyWindow(QMainWindow):
    # 构造函数
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        # 类初始化
        self.guide = Guide()
        self.buy_list = Buy_Item_List()
        # 设置窗口
        self.ui = Ui_main.Ui_MainWindow()
        self.app = QApplication(sys.argv)
        self.ui.setupUi(self)
        self.showFullScreen()
        # 事件绑定
        self.ui.button_debug_1.clicked.connect(self.exit)
        self.ui.button_debug_2.clicked.connect(self.debug_2)
        self.ui.button_debug_3.clicked.connect(self.debug_3)
        self.ui.button_add_guide_list.clicked.connect(self.open_qrcode_dialog)
        # 多线程
        self.qrcode_thread = QRCodeThread()
        self.qrcode_thread.signal.connect(self.qrcode_thread_callback)
        self.qrcode_thread.start()

    # 识别线程callback
    def qrcode_thread_callback(self, item):
        """
        扫描线程收到信号后的处理
        :param item:
        :return:
        """
        self.buy_list_add_item(Item(
            itemid=item.id,
            price=item.price,
            name=item.name
        ))

    def open_qrcode_dialog(self):
        # 添加购买列表
        def guide_list_refresh(guide_list):
            """
            读取预购的列表 *暂时从已购买的列表中读取
            :return:
            """
            self.guide.set_list(guide_list)
            self.guide.list.sorted()
            if self.guide.get_list():
                for item in self.guide.get_list():
                    self.guide_list_add_ui(item)
                self.ui.label_guide_item_name.setText(f'{self.guide.get_list()[0].name}')
                self.ui.label_guide_item_area.setText(f'{self.guide.get_list()[0].area}')
            print(f"qrcode_dialog return:{guide_list}")

        qrcode_dialog = QRcode_dialog.QRcode_dialog()
        qrcode_dialog.signal.connect(guide_list_refresh)
        qrcode_dialog.exec_()

    # debug 按键
    def exit(self):  # 退出按钮
        self.qrcode_thread.terminate()
        self.app.quit()

    def debug_2(self):
        self.buy_list_add_item(Item(
            itemid=0,
            name="衬衫",
            price=99.9

        ))

    def debug_3(self):
        for i in range(3):
            self.buy_list_add_item(Item(itemid=i + 1, name="蔡徐坤", price=100, num=4))

    def buy_list_add_item(self, item):
        """
        从结算列表里添加一个item
        :param item:
        :return:
        """
        self.buy_list.add_item(item)
        self.ui.label_price.setText(f'{round(item.price, 2)} 元')
        self.ui.label_title.setText(f'{item.name}')
        self.ui.tabWidget.setCurrentIndex(1)
        # 判断添加的物品是否在导购列表里
        if self.guide.list.in_list(item.id):
            print(f"{item.id}他在里面")
            self.guide.list.reduce_item_from_id(item.id, item.num)
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
        print(self.buy_list.all_price)
        if self.buy_list.all_price == 0:
            self.ui.label_all_price.setText(f'0 元')

    # 添加列表
    def buy_list_add_ui(self, item: Item):
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

    def guide_list_add_ui(self, item: Item):
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
