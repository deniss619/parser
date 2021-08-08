"""Спарсите все анекдоты из определенного раздела сайта https://anekdoty.ru/
Сохраните их в базу данных. При сохранении очистите их от лишних тегов.
Добавлена многопоточность для уменьшения времени паринга"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from selenium import webdriver
import math
from threading import Thread
from datetime import datetime

connection = psycopg2.connect("postgresql://postgres:1234@localhost:5432/jokes")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
table_name = "ex6"


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--start-maximized")
    return webdriver.Chrome(options=chrome_options)


def get_jokes_from_page(driver, category):
    jokes = driver.find_elements_by_xpath("//ul[@class='item-list']/li")
    for joke in jokes:
        text = joke.find_element_by_xpath(".//p").text.replace("'", "''")
        query = f"""INSERT INTO {table_name}(category, joke, time) VALUES ('{category}','{text}','{datetime.now().time()}')"""
        cursor.execute(query)
        connection.commit()


def parse_category(category):
    driver = get_driver()
    try:
        driver.get(category['url'])
        total = int(driver.find_element_by_xpath("//div[@class='total']/span").text)
        url = driver.current_url
        for page_number in range(1, math.ceil(total / 15) + 1):
            driver.get(url + f"page/{page_number}/")
            get_jokes_from_page(driver, category['name'])
    except:
        pass
    finally:
        driver.close()


driver = get_driver()
driver.get('https://anekdoty.ru/')
categories = driver.find_elements_by_xpath("//ul[@class='list']/li")

categories = [{'name': category_url.find_element_by_xpath('.//span/a').get_attribute('innerText').replace(",",
                                                                                                          "").replace(
    " ", "_"), 'url': category_url.find_element_by_xpath('.//span/a').get_attribute('href')} for category_url in
    categories]

for category in categories:
    th = Thread(target=parse_category, args=(category,))
    th.start()

driver.close()
