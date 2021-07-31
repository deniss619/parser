"""Зайдите на следующую страницу http://planetolog.ru/city-world-list.php и спарсите ссылки на все страны мира,
зайдите в каждую страну, спарсите ее города, зайдите в каждый город и спарсите описание этого города.
Сохраните описание городов в базу данных. Страны для этих городов храните в отдельной таблице."""

import psycopg2
import requests
from bs4 import BeautifulSoup

connection = psycopg2.connect("postgresql://postgres:1234@localhost:5432/parser")
cursor = connection.cursor()
table_name = 'ex4'
cursor.execute(f"""SELECT EXISTS(SELECT 1 FROM information_schema.tables 
              WHERE table_catalog='parser' AND 
                    table_schema='public' AND 
                    table_name='{table_name}_countries')""")

if not cursor.fetchone()[0]:
    query = f'''CREATE TABLE {table_name}_countries(
           id SERIAL PRIMARY KEY,
           name TEXT
        )'''
    cursor.execute(query)
    query = f'''CREATE TABLE {table_name}_cities(
               id SERIAL PRIMARY KEY,
               name TEXT,
                country_id INTEGER,
                description TEXT,
                FOREIGN KEY (country_id) REFERENCES ex4_countries (id)
            )'''
    cursor.execute(query)
    connection.commit()
def get_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return [j for i in soup.find_all('div', class_='textplane')[1].find('table').find_all('tr')[1:] for j in i.find_all('a')]


countries = get_info("http://planetolog.ru/city-world-list.php")
for country in countries:
    query = f"""INSERT INTO {table_name}_countries(name) VALUES ('{country.text.replace("'", "''")}')"""
    # cursor.execute(query)
    # connection.commit()
    cities = get_info('http://planetolog.ru/' + country['href'])
    for city in cities:
        r = requests.get('http://planetolog.ru/' + city['href'])
        soup = BeautifulSoup(r.text, "lxml")
        a = soup.find_all('div', class_='textplane')[1].find('p')
        query = f"""INSERT INTO {table_name}_cities (name, country_id, description) VALUES
                ('{city.text.replace("'", "''")}', {countries.index(country) + 1},'{a.text.replace("'", "''")}')"""
        # cursor.execute(query)
        # connection.commit()

connection.commit()
connection.close()
cursor.close()