from pymongo import MongoClient

def connection():
    host = 'master'  # 你的ip地址
    client = MongoClient(host, 27017)  # 建立客户端对象
    db = client.zhaopinwangzhan  # 连接mydb数据库，没有则自动创建
    myset = db['zhilian']  # 使用test_set集合，没有则自动创建
    return myset

def get_Data():
    c = connection()
    res_list = []
    for zhilian in c.find():
        res_list.append(zhilian)
    return res_list