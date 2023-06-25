#更新数据
import ConnectionMongodb

collection = ConnectionMongodb.connection()

# 更新数据
for i in collection.find():
    query  = {
        "_id": i['_id']
    }
    money = i['money']

    try :
        if money == '面议':
            money = 0.0
        else:
            money = money.split("-")[0]
            if "万" in money:
                money = float(money.split("万")[0]) * 10000
            else:
                money = float(money.split("千")[0]) * 1000
    except Exception as e:
        continue
    update_query = {"$set": {"money": money}}
    collection.update_one(query, update_query)
