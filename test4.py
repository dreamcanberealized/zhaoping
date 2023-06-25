import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient
plt.rcParams['font.sans-serif'] = ['STSong']
plt.rcParams['axes.unicode_minus'] = False
# 连接MongoDB数据库
#更新数据
import ConnectionMongodb

collection = ConnectionMongodb.connection()

# 从MongoDB中获取数据
data = list(collection.find().limit(1000))
df = pd.DataFrame(data)
df['money'] = df['money'].astype(int)
#
# 进行多维度分析
# 计算岗位数量
job_count = df['zhiwei'].value_counts().sample(n=5)

# 计算平均薪资
mean_salary = df.groupby('zhiwei')['money'].mean().sample(n=5)

# 计算最高薪资
max_salary = df.groupby('zhiwei')['money'].max().sample(n=5)

# 计算最低薪资
min_salary = df.groupby('zhiwei')['money'].min().sample(n=5)
# 设置子图布局
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

# 绘制岗位数量的柱状图
axes[0, 0].bar(job_count.index, job_count.values)
axes[0, 0].set_xlabel('岗位名称')
axes[0, 0].set_ylabel('招聘总数量')
axes[0, 0].set_title('岗位数量分布')
axes[0, 0].tick_params(axis='x', rotation=45)

# 绘制平均薪资的柱状图
axes[0, 1].bar(mean_salary.index, mean_salary.values)
axes[0, 1].set_xlabel('岗位名称')
axes[0, 1].set_ylabel('平均薪资')
axes[0, 1].set_title('岗位平均薪资分布')
axes[0, 1].tick_params(axis='x', rotation=45)

# 绘制最高薪资的柱状图
axes[1, 0].bar(max_salary.index, max_salary.values)
axes[1, 0].set_xlabel('岗位名称')
axes[1, 0].set_ylabel('最高薪资')
axes[1, 0].set_title('岗位最高薪资分布')
axes[1, 0].tick_params(axis='x', rotation=45)

# 绘制最低薪资的柱状图
axes[1, 1].bar(min_salary.index, min_salary.values)
axes[1, 1].set_xlabel('岗位名称')
axes[1, 1].set_ylabel('最低薪资')
axes[1, 1].set_title('岗位最低薪资分布')
axes[1, 1].tick_params(axis='x', rotation=45)

# 调整子图之间的间距
plt.tight_layout()

# 显示图像
plt.show()