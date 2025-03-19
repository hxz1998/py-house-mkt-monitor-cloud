import os
import sqlite3
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def generate_graph(db_path):
    # 确保 ./report/ 目录存在
    os.makedirs('./report', exist_ok=True)

    # 连接到SQLite数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询每个 statistics_date 下的最新一条数据
    query = """
    SELECT statistics_date, date_time, subscription_sets, deals_sets
    FROM house_mkt_data
    WHERE (statistics_date, date_time) IN (
        SELECT statistics_date, MAX(date_time)
        FROM house_mkt_data
        GROUP BY statistics_date
    )
    ORDER BY statistics_date
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    # 准备数据
    statistics_dates = []
    subscription_sets = []
    deals_sets = []

    for row in rows:
        statistics_dates.append(datetime.strptime(row[0], '%Y-%m-%d').date())
        subscription_sets.append(row[2])
        deals_sets.append(row[3])

    # 绘制图表
    plt.figure(figsize=(26, 15))

    # 绘制 subscription_sets 折线图
    plt.plot(statistics_dates, subscription_sets, label='subscription sets', marker='o', color='blue')

    # 标注 subscription_sets 的数据点
    for i, (date, value) in enumerate(zip(statistics_dates, subscription_sets)):
        plt.text(date, value, f'{value}', fontsize=16, ha='right', va='bottom', color='blue')

    # 绘制 deals_sets 折线图
    plt.plot(statistics_dates, deals_sets, label='deals sets', marker='o', color='red')

    # 标注 deals_sets 的数据点
    for i, (date, value) in enumerate(zip(statistics_dates, deals_sets)):
        plt.text(date, value, f'{value}', fontsize=16, ha='left', va='top', color='red')

    # 设置横坐标格式
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gcf().autofmt_xdate()

    # 添加标题和标签
    plt.title('Subscription sets and deals sets over time', fontsize=18)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    # 添加图例
    plt.legend(fontsize=12)
    plt.grid(visible=True)

    # 保存图表到本地
    plt.savefig('./report/house_mkt_data_plot.png', bbox_inches='tight')
    # 显示图表
    plt.show()

    # 关闭数据库连接
    conn.close()
