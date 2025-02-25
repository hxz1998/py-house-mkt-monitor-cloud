import sqlite3
from loguru import logger


def fetch_data_from_db(db_path, table_name):
    # 连接到SQLite数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 获取表结构信息
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    # 获取表中的所有数据
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return column_names, rows


def generate_markdown(column_names, rows, exclude_column=None):
    # 如果需要排除某一列，找到它的索引并过滤掉
    # 生成Markdown表格的标题行
    markdown = "| " + " | ".join(column_names) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(column_names)) + " |\n"

    # 生成Markdown表格的数据行
    for row in rows:
        markdown += "| " + " | ".join(map(str, row)) + " |\n"

    return markdown


def save_markdown_to_file(markdown, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown)


def generate_report(db_path, table_name):
    # 从数据库中获取数据
    column_names, rows = fetch_data_from_db(db_path, table_name)

    # 输出Markdown文件的路径
    output_file = './report.md'

    # 生成Markdown文本
    markdown = generate_markdown(column_names, rows)

    # 将Markdown文本保存到文件
    save_markdown_to_file(markdown, output_file)

    logger.info(f"报告已生成: {output_file}")
