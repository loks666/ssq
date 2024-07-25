import asyncio
import os
import time

import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 判断当前操作系统
is_windows = os.name == 'nt'

# 数据库配置
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '数据库密码' if is_windows else '数据库密码!',
    'database': 'lottery'
}

wait_time = 15

# 全局 WebDriver 变量
driver = None


def init_driver():
    global driver
    # 初始化 WebDriver
    chrome_driver_path = "./chromedriver.exe" if is_windows else "./chromedriver"
    plugin_path = "./xpathHelper.crx"

    options = webdriver.ChromeOptions()
    # 如果你有插件需要加载，请取消下一行的注释
    options.add_extension(plugin_path)
    # 如果需要无头模式，请取消下一行的注释
    options.add_argument("--headless")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def fetch_data():
    global driver
    driver = init_driver()
    # 打开目标网址
    url = 'https://www.zhcw.com/kjxx/ssq/'
    driver.get(url)

    # 等待页面加载完成
    time.sleep(3)  # 适当增加等待时间，确保页面加载完全

    # 确认浏览器窗口是否打开
    print("浏览器打开成功")

    # 查找包含数据的表格行
    rows = driver.find_elements(By.XPATH, '//tr[@data-zhou]')
    print(f"找到 {len(rows)} 行包含 data-zhou 属性的数据")

    data = []
    for row in rows:
        item = {
            '期号': row.find_element(By.XPATH, './td[1]').text,
            '开奖日期': row.find_element(By.XPATH, './td[2]').text,
            '红球号码': [span.text for span in row.find_elements(By.XPATH, './td[3]//span[@class="jqh"]')],
            '蓝球号码': row.find_element(By.XPATH, './td[4]//span[@class="jql"]').text,
            '销售额': row.find_element(By.XPATH, './td[5]').text,
            '一等奖数': row.find_element(By.XPATH, './td[6]').text,
            '一等奖奖金': row.find_element(By.XPATH, './td[7]').text,
            '二等奖数': row.find_element(By.XPATH, './td[8]').text,
            '二等奖奖金': row.find_element(By.XPATH, './td[9]').text,
            '三等奖数': row.find_element(By.XPATH, './td[10]').text,
            '三等奖奖金': row.find_element(By.XPATH, './td[11]').text,
            '奖池': row.find_element(By.XPATH, './td[12]').text,
        }
        data.append(item)
        print(item)

    return data


def get_latest_issue_number():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT issue_number FROM ssq ORDER BY issue_number DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        connection.close()


def insert_data(data):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            for item in data:
                cursor.execute("""
                    INSERT INTO ssq (issue_number, draw_date, red1, red2, red3, red4, red5, red6, blue, total_sales,
                                     first_prize_count, first_prize_amount, second_prize_count, second_prize_amount,
                                     third_prize_count, third_prize_amount, prize_pool)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (item['期号'], item['开奖日期'], item['红球号码'][0], item['红球号码'][1], item['红球号码'][2],
                          item['红球号码'][3], item['红球号码'][4], item['红球号码'][5], item['蓝球号码'],
                          item['销售额'], item['一等奖数'], item['一等奖奖金'], item['二等奖数'], item['二等奖奖金'],
                          item['三等奖数'], item['三等奖奖金'], item['奖池']))
        connection.commit()
    finally:
        connection.close()


async def main():
    global driver

    # 从数据库中获取最新的期号
    latest_issue_number = get_latest_issue_number()
    print(f"数据库中的最新期号: {latest_issue_number}")

    # 从网页中获取数据
    fetched_data = fetch_data()

    # 过滤新的数据
    new_data = [item for item in fetched_data if int(item['期号']) > int(latest_issue_number)]

    if new_data:
        insert_data(new_data)
        print(f"插入了 {len(new_data)} 条新记录到数据库。")
    else:
        print("没有找到新数据。")

    # 关闭浏览器
    driver.quit()


if __name__ == "__main__":
    asyncio.run(main())
