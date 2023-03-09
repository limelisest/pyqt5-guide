from event.item import Item


class Guide:

    def __init__(self):
        self._map = [
            # A B  C  D  E  F  G  H  I  J  K  L  M  N  O  P
            # 0 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],  # 2
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 3
            [0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 4
            [0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 5
            [0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 6
            [0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 7
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0],  # 8
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],  # 9
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 10
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],  # 11
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],  # 12
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 13
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 14
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 15
        ]  # 这一段没用，先放着，以后也可能没用
        self._start = [0, 10]
        self._list = self.List([], self._start)

    def set_map(self, _map):
        self._map = _map

    def set_list(self, _list):
        self._list = self.List(_list, self._start)

    def set_start(self, _start):
        self._list = _start

    @property
    def start(self):
        return self._start

    @property
    def list(self):
        return self._list

    def get_list(self):
        return self._list.list

    # 列表类
    class List:

        def __init__(self, _list, _start):
            self._list: list = _list
            self._start = _start

        def sort(self):
            """
            按照距离排序需要购买物品的列表，每到达一个新的点就会以当前作为起点重新计算
            :return: [item1,item2,...,item]
            """
            temp = Item(itemid=-1)
            _start_temp = self._start
            temp_list = []
            start_list = self._list
            count = 0
            while start_list:
                count += 1
                temp_min = 999999
                x_s, y_s = _start_temp
                for line in start_list:
                    x, y = line.area
                    _sum = (((x - x_s) ** 2) + ((y - y_s) ** 2)) ** 0.5
                    if _sum <= temp_min:
                        temp_min = _sum
                        temp = line
                print(f"{count}.[Start Point]<{_start_temp}>,[Next Point]<{temp.area}>")
                temp_list.append(temp)
                start_list.remove(temp)
                _start_temp = temp.area

            return temp_list

        def sorted(self):
            """
            自身对象内的列表按照顺序重新排列
            :return: none
            """
            self._list = self.sort()

        def reduce_item_from_id(self, itemid, num):
            """
            指定itemid，减少预购列表中的数量直到删除
            :param num: int
            :param itemid: int
            :return:
            """
            for item in self._list:
                if itemid == item.id:
                    item.reduce_num(num)
                    if item.num <= 0:
                        self._list.remove(item)

        def in_list(self, itemid):
            for item in self._list:
                if itemid == item.id:
                    return True
            return False

        def print(self):
            line: Item  # line 是一个Item类型的对象
            temp = ''
            for line in self._list:
                temp += f'id:{line.id},name:{line.name},price:{line.price},num:{line.num},area:{line.area}\n'
            return temp

        @property
        def list(self):
            return self._list

    @property
    def map(self):
        return self._map
