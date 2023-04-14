import os
import uuid

dir_name = './device'
file_name = '/uuid.txt'
user_id = 'anonymous'


def get_uuid():
    if not os.path.exists(dir_name):  # 检测输出的文件夹是否存在
        os.mkdir(dir_name)
    if not os.path.exists(f'{dir_name}{file_name}'):  # 检测文件是否存在,不存在则创建文件并初始化uuid
        file = open(f'{dir_name}{file_name}', 'w', encoding='utf-8', )
        _uuid = uuid.uuid4()
        file.write(f'{_uuid}')
    file = open(f'{dir_name}{file_name}', 'r', encoding='utf-8', )
    _uuid = file.read()
    return _uuid


def reset_uuid():
    os.remove(f'{dir_name}{file_name}')
    get_uuid()


def get_network_name():
    pass
