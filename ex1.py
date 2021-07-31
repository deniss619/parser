import psycopg2
from selenium import webdriver

"""Зайдите на следующую страницу: 
http://old.code.mu/exercises/advanced/php/parsing/poetapnyj-parsing-i-metod-pauka/1/index.php
Сделайте парсер, который заберет все ссылки из главного меню, затем перейдет по каждой из них, спарсит содержимое 
контента страниц и сохранит в базу данных контент страницы, тайтл страницы, url страницы."""


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--start-maximized")
    return webdriver.Chrome(options=chrome_options)


connection = psycopg2.connect("postgresql://postgres:1234@localhost:5432/parser")
cursor = connection.cursor()
driver = get_driver()
driver.get("http://old.code.mu/exercises/advanced/php/parsing/poetapnyj-parsing-i-metod-pauka/1/index.php")
menu = driver.find_elements_by_xpath("//div[@id='menu']/ul/li")

hrefs = list(map(lambda i: i.find_element_by_xpath(".//a").get_attribute('href'), menu))

for url in hrefs:
    driver.get(url)
    content = driver.find_element_by_id("content").text
    insert_query = f"""INSERT INTO ex1(title, url, content) VALUES ('{driver.title}', '{url}', '{content}')"""
    cursor.execute(insert_query)

connection.commit()
driver.close()
