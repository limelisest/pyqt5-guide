import pymysql
from event.item import Item

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

    def get_item_from_id(self, _itemid):
        """
        通过物品id从数据库获取该物品的信息
        :param _itemid:物品ID
        :return: Item
        """
        cursor = self.connect.cursor()
        sql = f'''
        select * from item where id = {_itemid}
        '''
        cursor.execute(sql)

        sql_data: dict = cursor.fetchone()

        item = Item(
            itemid=sql_data['id'],  # 数据库主键
            qrcode_id=sql_data['qrcode_id'],  # 二维码
            bar_code_id=sql_data['bar_code_id'],  # 条形码
            rf_id=sql_data['rf_id'],  # RFID
            name=sql_data['name'],  # 名字
            price=sql_data['price'],  # 价格
            area=[sql_data['area_x'], sql_data['area_y']],  # 坐标
            info=sql_data['info']  # 信息
        )
        return item
