"""Спарсите все анекдоты из определенного раздела сайта https://anekdoty.ru/
Сохраните их в базу данных. При сохранении очистите их от лишних тегов."""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from selenium import webdriver
import math

connection = psycopg2.connect("postgresql://postgres:1234@localhost:5432")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
table_name = "ex6"

cursor.execute("SELECT 1 FROM pg_database WHERE datname='jokes'")
if cursor.fetchone() is None:
    cursor.execute(f"""CREATE DATABASE jokes""")

    connection = psycopg2.connect("postgresql://postgres:1234@localhost:5432/jokes")
    cursor = connection.cursor()
    query = f'''CREATE TABLE {table_name}(
           id SERIAL PRIMARY KEY,
            category TEXT,
           joke TEXT
        )'''
    cursor.execute(query)


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
    for i in jokes:
        a = i.find_element_by_xpath(".//p")
        query = f"""INSERT INTO {table_name}(category, joke) VALUES ('{category}','{a.text.replace("'", "''")}')"""
        cursor.execute(query)
        connection.commit()


driver = get_driver()
driver.get('https://anekdoty.ru/')
categories = driver.find_elements_by_xpath("//ul[@class='list']/li")

categories = [{'name': category_url.find_element_by_xpath('.//span/a').get_attribute('innerText').replace(",",
                                                                                                          "").replace(
    " ", "_"), 'url': category_url.find_element_by_xpath('.//span/a').get_attribute('href')} for category_url in
    categories]

for i in categories:
    driver.get(i['url'])
    total = int(driver.find_element_by_xpath("//div[@class='total']/span").text)
    url = driver.current_url
    for page_number in range(1,math.ceil(total/15)+1):
        driver.get(url+f"page/{page_number}/")
        get_jokes_from_page(driver, i['name'])

driver.close()
