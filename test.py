import ConnectionMongodb

collection = ConnectionMongodb.connection()
data = collection.find().limit(100)
res_list = []
pipeline = [
    # 排除 面议 和空的
    {
        "$match": {
            "$and": [
                {"money": {"$ne": "面议"}},
            ]
        }
    },
    {
    "$project": {
    "salary": {
    "$arrayElemAt": [
    { "$split": ["$money", "-"]},0]
    }
    }
    },
# {
#     "$addFields": {
#       "parsed_salary": {
#         "$cond": {
#           "if": { "$regexMatch": { input: "$salary", regex: /万$/ } },
#           "then": { "$toDouble": { "$trim": { input: { "$replaceOne": { input: "$salary", find: "万", replacement: "" } } } } },
#           "else": { "$multiply": [{ "$toDouble": { $trim: { input: { $replaceOne: { input: "$salary", find: "千", replacement: "" } } } } }, 10] }
#         }
#       }
#     }
#   }
    {"$limit": 100}
]

job_data = list(collection.aggregate(pipeline))

job_titles = [item['_id'] for item in job_data]
total_count = [item['total_count'] for item in job_data]
average_salary = [item['average_salary'] for item in job_data]
max_salary = [item['max_salary'] for item in job_data]
min_salary = [item['min_salary'] for item in job_data]
print(total_count)
print(max_salary)
print(min_salary)
print(average_salary)
