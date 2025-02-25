from loguru import logger
from house_mkt_monitor.core.crawler import crawl_data
from house_mkt_monitor.core.config import house_mkt_data_url
from house_mkt_monitor.core.db_writer import save
import os

if __name__ == '__main__':
    logger.info("服务启动……")
    logger.info("准备拉取数据")
    data = crawl_data(house_mkt_data_url)
    logger.info("拉取数据完成，进行存储")
    db = os.path.abspath(os.path.dirname(__file__) + "/database/data.db")
    save(data, db)
    logger.info("存储完成")
