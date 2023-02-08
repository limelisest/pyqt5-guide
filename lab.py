# import pymysql
#
# _ip = '120.79.71.233'
# _port = 3306
# db_name = 'guide'
# db_user = 'guide'
# db_password = 'lime'
#
# conn = pymysql.connect(
#     host=_ip,
#     port=_port,
#     database=db_name,
#     user=db_user,
#     passwd=db_password,
#     charset='utf8mb4'
# )
# cur = conn.cursor()
# sql = 'select * from item'
# cur.execute(sql)
# print("显示创建的表：", cur.fetchall())

from event.sql import MySQl
from event.item import Item

sql = MySQl()
item: Item = sql.get_item_from_id(0)
item.print()
