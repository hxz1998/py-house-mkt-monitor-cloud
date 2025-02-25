import sqlite3
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from loguru import logger


def save(data: dict, db: str):
    # 定义东八区时区
    tz = ZoneInfo('Asia/Shanghai')

    # 获取当前时间并转换为东八区时间
    beijing_time = datetime.now(tz)

    # 获取日期部分
    beijing_date = beijing_time.date()
    logger.info(f"北京时间：{beijing_date}-{beijing_time}")

    subscription_sets = data['商品房交易数据']['认购套数']
    deals_sets = data['商品房交易数据']['成交套数']
    city_projects_oneline = data['楼盘供应情况']['全市入网项目']
    city_area_online = data['楼盘供应情况']['全市入网面积']
    yearly_listed_area = data['楼盘供应情况']['本年上市']
    yearly_deals_area = data['楼盘供应情况']['本年成交']
    monthly_listed_area = data['楼盘供应情况']['本月上市']
    monthly_deals_area = data['楼盘供应情况']['本月成交']
    raw_text = str(data)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
                INSERT INTO house_mkt_data (
                statistics_date, 
                date_time, 
                subscription_sets, 
                deals_sets, 
                city_projects_oneline, 
                city_area_online, 
                yearly_listed_area, 
                yearly_deals_area, 
                monthly_listed_area, 
                monthly_deals_area, 
                raw_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (beijing_date, beijing_time, subscription_sets, deals_sets, city_projects_oneline,
                  city_area_online, yearly_listed_area, yearly_deals_area, monthly_listed_area, monthly_deals_area,
                  raw_text))
    conn.commit()
    conn.close()
