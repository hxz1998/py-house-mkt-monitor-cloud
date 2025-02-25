import requests
from bs4 import BeautifulSoup
from loguru import logger


def crawl_data(house_mkt_data_url):
    # 获取网页内容
    html = fetch_html(house_mkt_data_url)
    if not html:
        logger.error("无法获取网页内容")
        return

    # 解析网页内容
    result = parse_html(html)
    if not result:
        logger.error("解析失败")
        return
    return result


# 发送 HTTP 请求，获取网页内容
def fetch_html(house_mkt_data_url):
    try:
        response = requests.get(house_mkt_data_url)
        response.encoding = 'utf-8'
        response.raise_for_status()  # 检查请求是否成功
        return response.text  # 返回网页的 HTML 内容
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败: {e}")
        return None


# 解析 HTML 内容
def parse_html(html):
    if not html:
        return None

    # 创建 BeautifulSoup 对象
    soup_instant = BeautifulSoup(html, 'html.parser')

    # 提取认购和成交套数
    def parse_transaction_data(soup):
        transaction = {}
        box = soup.find(class_='busniess_num_box')
        if not box:
            return None

        items = box.find_all(class_='busniess_num_mian')
        if len(items) < 2:
            return None

        # 认购套数
        subscribe_div = items[0].find(class_='busniess_num_word')
        if subscribe_div:
            transaction['认购套数'] = int(subscribe_div.get_text(strip=True))

        # 成交套数
        deal_div = items[1].find(class_='busniess_num_word')
        if deal_div:
            transaction['成交套数'] = int(deal_div.get_text(strip=True))

        return transaction

    # 解析表格数据
    def parse_table_data(soup):
        table_data = {}
        table = soup.find('table', class_='table grayTh mt-2')
        if not table:
            return None
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) != 4:
                continue
            # 处理每行的两组数据
            keys = [tds[0].get_text(strip=True), tds[2].get_text(strip=True)]
            values = [tds[1].get_text(strip=True), tds[3].get_text(strip=True)]
            for key, value in zip(keys, values):
                # 提取数值
                num = ''.join(filter(lambda x: x.isdecimal() or x == '.', value))
                if num:
                    if '.' in num:
                        table_data[key] = str(num)
                    else:
                        table_data[key] = str(num)
        return table_data

    # 组合所有数据
    result = {
        '商品房交易数据': parse_transaction_data(soup_instant),
        '楼盘供应情况': parse_table_data(soup_instant)
    }

    return result
