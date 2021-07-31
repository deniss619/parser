"""Зайдите на следующую страницу:
http://old.code.mu/exercises/advanced/php/parsing/poetapnyj-parsing-i-metod-pauka/2/index1.php
Сделайте парсер, который заберет все ссылки из пагинации, затем перейдет по каждой из них, заберет все ссылки на статьи,
а затем зайдет на каждую из статей. Сохраните в базу данных страницы со статьями (промежуточные не нужны).
А именно: контент страницы, тайтл страницы, url страницы."""

import psycopg2
from selenium import webdriver


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--start-maximized")
    return webdriver.Chrome(options=chrome_options)


driver = get_driver()
driver.get("http://old.code.mu/exercises/advanced/php/parsing/poetapnyj-parsing-i-metod-pauka/2/index1.php")

connection = psycopg2.connect("postgresql://postgres:1234@localhost:5432/parser")
cursor = connection.cursor()

cursor.execute("""SELECT EXISTS(SELECT 1 FROM information_schema.tables 
              WHERE table_catalog='parser' AND 
                    table_schema='public' AND 
                    table_name='ex2')""")

if not cursor.fetchone()[0]:
    query = '''CREATE TABLE ex2(
           id SERIAL PRIMARY KEY,
           title TEXT,
           url TEXT,
           content TEXT
        )'''
    cursor.execute(query)

pages = driver.find_elements_by_xpath("//div[@id='menu']/ul/li")

hrefs = list(map(lambda i: i.find_element_by_xpath(".//a").get_attribute("href"), pages[1:-1]))
topics = []
for pageUrl in hrefs:
    driver.get(pageUrl)
    topicUrl = driver.find_elements_by_xpath("//div[@id='main']/h2")
    for i in topicUrl:
        topics.append(i.find_element_by_xpath(".//a").get_attribute("href"))

for topic in topics:
    driver.get(topic)
    content = driver.find_element_by_id("main").text
    insert_query = f"""INSERT INTO ex2(title, url, content) VALUES ('{driver.title}', '{topic}', '{content}')"""
    cursor.execute(insert_query)
connection.commit()
connection.close()
cursor.close()
driver.close()
