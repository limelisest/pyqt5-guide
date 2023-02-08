from decimal import Decimal


class Item:
    def __init__(self, itemid, qrcode_id=None, rf_id=None, bar_code_id=None, name="unknown", info="unknown", area=None,
                 price=0, num=1):
        if area is None:
            area = [-1, -1]
        self.id = itemid
        self.qrcode_id = qrcode_id
        self.bar_code_id = bar_code_id
        self.rf_id = rf_id
        self.name = name
        self.info = info
        self.area = area
        self.price = price
        self.num = num

    def set_num(self, num):
        self.num = num

    def add_num(self, add_num):
        self.num += add_num

    def print(self):
        print(f'''
        id:{self.id}
        qrcode_id:{self.qrcode_id}
        bar_code_id:{self.bar_code_id}
        rfid:{self.rf_id}
        name:{self.name}
        info:{self.info}
        price:{self.price}
        area:{self.area}
        num:{self.num}
        ''')


class Buy_Item_List:  # 购买列表处理类
    def __init__(self):
        self.list = {}
        self.all_price = 0

    # 往列表添加一个item
    def add_item(self, item: Item):
        if item.id in self.list.keys():
            self.list[item.id].add_num(item.num)
        else:
            self.list[item.id] = item
        self.refresh_all_price()
        return item

    # 从指定的itemid减少一个数量
    def reduce_item_from_id(self, itemid):
        item_list = self.list[itemid]
        if item_list.num > 1:
            self.list[itemid].num -= 1
        else:
            del self.list[itemid]
        self.refresh_all_price()
        return itemid

    # 重新计算总价值
    def refresh_all_price(self):
        temp = 0
        buy_list = self.list
        if buy_list:
            for i in buy_list:
                temp += round(Decimal(buy_list[i].price) * Decimal(buy_list[i].num), 2)
        self.all_price = temp
