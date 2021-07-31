"""Спарсите названия всех фильмов из определенного раздела сайта https://www.kinopoisk.ru/
Сохраните эти названия в базу данных."""
from selenium import webdriver


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--start-maximized")
    return webdriver.Chrome(options=chrome_options)


# driver = get_driver()
# driver.get('https://www.kinopoisk.ru/')
#
# a = driver.find_elements_by_xpath("//a[(text()='Топ 250')]")[1]
# a.click()
# driver.find_elements_by_class_name('_1qw3ltaJ1A8fhSN7wPDgbL')
#
# driver.close()

a1 = """/html[@class='ua_js_no app-theme_light']/body[@class='body body_app-width_wide body_app-theme_light']
/div[@class='app-container app-container_app-theme_light']/div[@class='app app_app-theme_light app_app-width_wide app_header-theme_topline']
/div[@class='app__content app__content_app-width_wide app__content_app-theme_light']/div[@class='app__page app__page_app-theme_light']
/div[@class='R3wWj7bbDbKX9NzLqhYCM _2HZ5VvzrzSn8w7y6vQGuOh']/div[@class='_2pg46b7pEErCqdM94TauPn'][2]
/div[@class='D-J_v-z-wQu8erXIT_VDW _8AvDyin2vhiHmsIW_pwJ6 fuuDrdTUzw4Wk6tkeIjjL']/main[@class='_1hVe_aOJQ1rTCOcsmpFPSe']
/div[2]/div[@class='selection-list']/div[@class='desktop-rating-selection-film-item'][1]/div[@class='desktop-rating-selection-film-item__content-wrapper']
/div[@class='desktop-rating-selection-film-item__upper-wrapper']/div[@class='desktop-rating-selection-film-item__meta-wrapper']
/div[@class='selection-film-item-meta selection-film-item-meta_theme_desktop']/a[@class='selection-film-item-meta__link']/p[@class='selection-film-item-meta__name']"""

a2 = """/html[@class='ua_js_no app-theme_light']/body[@class='body body_app-width_wide body_app-theme_light']/div[@class='app-container app-container_app-theme_light']
/div[@class='app app_app-theme_light app_app-width_wide app_header-theme_topline']/div[@class='app__content app__content_app-width_wide app__content_app-theme_light']
/div[@class='app__page app__page_app-theme_light']/div[@class='R3wWj7bbDbKX9NzLqhYCM _2HZ5VvzrzSn8w7y6vQGuOh']
/div[@class='_2pg46b7pEErCqdM94TauPn'][2]/div[@class='D-J_v-z-wQu8erXIT_VDW _8AvDyin2vhiHmsIW_pwJ6 fuuDrdTUzw4Wk6tkeIjjL']
/main[@class='_1hVe_aOJQ1rTCOcsmpFPSe']/div[2]/div[@class='selection-list']/div[@class='desktop-rating-selection-film-item'][2]
/div[@class='desktop-rating-selection-film-item__content-wrapper']/div[@class='desktop-rating-selection-film-item__upper-wrapper']
/div[@class='desktop-rating-selection-film-item__meta-wrapper']/div[@class='selection-film-item-meta selection-film-item-meta_theme_desktop']
/a[@class='selection-film-item-meta__link']/p[@class='selection-film-item-meta__name']"""
#
# for i in range(len(a1)):
#     if a1[i] != a2[i]:
#         print(a1[i:])
#         print(a2[i:])
import psycopg2

connection = psycopg2.connect("postgresql://postgres:1234@localhost:5432/parser")
cursor = connection.cursor()
# query = f'''CREATE TABLE dell(
#        id SERIAL PRIMARY KEY,
#        name TEXT
#     )'''
# cursor.execute(query)
# connection.commit()

a = "(('dsd'),('ddd'))"

print(a)
query = f"""INSERT INTO dell(name) VALUES {a}"""
cursor.execute(query)
connection.commit()
