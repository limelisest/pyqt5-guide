import calendar
import time

import pymysql
from event.item import Item
from event.device import user_id

_ip = '120.79.71.233'
_port = 3306
db_name = 'guide'
db_user = 'guide'
db_password = 'lime'


class MySQl:
    def __init__(self):
        self.connect = pymysql.connect(
            host=_ip,
            port=_port,
            database=db_name,
            user=db_user,
            passwd=db_password,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()

    def get_item(self, _id, _type="id"):
        """
        通过物品id从数据库获取该物品的信息
        :param _id:物品ID
        :param _type:id类型：id、bar_code_id、qrcode_id、rf_id
        :return: Item
        """
        cursor = self.connect.cursor()
        sql = f'''
        select * from item where {_type} = '{_id}'
        '''

        cursor.execute(sql)

        sql_data: dict = cursor.fetchone()
        if sql_data:
            item = Item(
                itemid=sql_data['id'],  # 数据库主键
                qrcode_id=sql_data['QRCODE'],  # 二维码
                bar_code_id=sql_data['EAN13'],  # 条形码
                rf_id=sql_data['RFID'],  # RFID
                name=sql_data['name'],  # 名字
                price=sql_data['price'],  # 价格
                area=[sql_data['area_x'], sql_data['area_y']],  # 坐标
                info=sql_data['info']  # 信息
            )
            return item
        else:
            return False

    def check_operator(self, _user, _password):
        print(f"【Operator Dialog】Enter:{_user},{_password}")
        cursor = self.connect.cursor()
        sql = f"select * from operator where user_name = '{_user}' and password = '{_password}'"

        cursor.execute(sql)

        sql_data: dict = cursor.fetchone()
        print(f'【Operator Dialog】{sql_data}')
        if sql_data:
            return sql_data['level']
        else:
            return False

    def change_operator(self, _user, old_password, new_password):
        if self.check_operator(_user, old_password):
            cursor = self.connect.cursor()
            try:
                # 修改密码
                sql = f"update operator set password = '{new_password}' where user_name='{_user}'"
                cursor.execute(sql)
                return True
            except pymysql.Error:
                return False
        else:
            return False

    def update_order(self, _list):
        cursor = self.connect.cursor()
        try:
            current_gmt = time.gmtime()
            time_stamp = calendar.timegm(current_gmt)
            for line in _list:
                item: Item = _list[line]
                item_id = item.id
                num = item.num
                sql = f"insert into order_history set " \
                      f"item_id='{item_id}',user_id='{user_id}',time='{time_stamp}',num='{num}'"
                cursor.execute(sql)
            return True
        except pymysql.Error:
            return False
