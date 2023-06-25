from flask import Flask, render_template, request
import math
import ConnectionMongodb
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
from matplotlib.ticker import MultipleLocator
app = Flask(__name__)
collection = ConnectionMongodb.connection()
plt.rcParams['font.sans-serif'] = ['STSong']
plt.rcParams['axes.unicode_minus'] = False

@app.route('/')
def index():
    # 分页
    page = request.args.get('page', default=1, type=int)
    per_page = 20
    # 总数量
    total_count = collection.count_documents({})
    # 总页数
    total_pages = math.ceil(total_count / per_page)
    # 开始索引
    start_idx = (page - 1) * per_page
    # 结束索引
    end_idx = start_idx + per_page
    # 拿数据
    page_data = list(collection.find().skip(start_idx).limit(per_page))
    return render_template('index.html', data=page_data, total_pages=total_pages, current_page=page)


@app.route('/city_stats')
def city_stats():
    # 使用聚合查询获得城市统计数据
    pipeline = [
        {"$group": {"_id": "$name", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ]
    city_stats = collection.aggregate(pipeline)

    return render_template('city_stats.html', city_stats=city_stats)
@app.route('/job')
def job():
    # 获取数据
    job_data = list(collection.find().limit(1000))

    # 进行多维度分析，生成图表
    job_titles =[]
    job_salaries = []
    for data in job_data:
        m = str(data['money'])
        if '元'  in m  or '千'  in m or '万' in m:
            continue
        job_salaries.append(data['money'])
        job_titles.append(data['zhiwei'].encode('utf-8'))

    job_salaries = random.sample(job_salaries, 6)
    job_titles = random.sample(job_titles, 6)
    # 将 job_salaries 数据类型转换为 int32
    job_salaries = np.array(job_salaries, dtype=np.int32)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(job_titles, job_salaries)
    ax.set_xlabel('职位', fontproperties='SimHei')
    ax.set_ylabel('薪资')
    plt.xticks(rotation=20)
    # 设置 x 轴刻度的间隔
    x_ticks_interval = 1
    ax.xaxis.set_major_locator(MultipleLocator(x_ticks_interval))

    # 将图表保存为图片文件
    img_path = 'static/chart.png'
    plt.savefig(img_path)

    # 渲染网页模板，并将图片路径传递给模板
    return render_template('job.html', chart_img=img_path)
#岗位
@app.route('/gangwei')
def gangwei():
    # 从MongoDB中获取数据
    data = list(collection.find().limit(1000))
    df = pd.DataFrame(data)
    # 计算岗位数量
    job_count = df['zhiwei'].value_counts().sample(n=5)
    # 绘制岗位数量的柱状图
    plt.figure(figsize=(16, 8))
    job_count.plot(kind='bar')
    plt.xlabel('岗位名称')
    plt.ylabel('招聘总数量')
    plt.title('岗位数量分布')
    plt.xticks(rotation=0)
    # 将图表保存为图片文件
    img_path = 'static/gangwei.png'
    plt.savefig(img_path)
    # 渲染网页模板，并将图片路径传递给模板
    return render_template('gangwei.html', chart_img=img_path)


@app.route('/money')
def money():
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

    # 将图表保存为图片文件
    img_path = 'static/money.png'
    plt.savefig(img_path)
    # 渲染网页模板，并将图片路径传递给模板
    return render_template('money.html', chart_img=img_path)

if __name__ == '__main__':
    app.run(debug=True)
