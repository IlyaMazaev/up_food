from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from tqdm.auto import tqdm

from data import db_session  # db engine

from main_recipes_api import add_new_product


def setDriver():  # Запуск драйвера
    driver = webdriver.Chrome()
    return driver


def parse_products(product_url, not_parsing_pages):  # Парсинг продуктов из категории
    db_session.global_init("../db/products_data.db")  # connecting to db

    driver = setDriver()
    driver.get(product_url)
    url_list = list()
    elements_of_types_of_food = driver.find_element(By.CSS_SELECTOR, '.catalog__list').find_elements(By.TAG_NAME,
                                                                                                     'a')  # Поиск всех категорий
    for i in tqdm(range(0, len(elements_of_types_of_food))):
        url_list.append(elements_of_types_of_food[i].get_attribute('href'))
    for i in tqdm(range(4, len(url_list))):
        if i in not_parsing_pages:
            continue
        driver.get(url_list[i])
        driver.implicitly_wait(5)
        elements_of_types_of_food_next = driver.find_elements(By.CSS_SELECTOR,
                                                              '.products-slider__header')  # Поиск всех под категорий
        sites_urls = list()
        for l in elements_of_types_of_food_next:
            sites_urls.append(l.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        for h in sites_urls:
            driver.get(h)  # Переход в подкатегорию
            driver.implicitly_wait(5)  # Проверка на загруженность страницы
            product_card = driver.find_elements(By.CSS_SELECTOR,
                                                '.sc-jrAGrp.kAEaPn')  # Поиск карточки продукта и названия категории
            type_of_product = driver.find_element(By.CSS_SELECTOR, '.page-header__title').text
            for k in product_card:  # Поиск названия, цены, ссылки на изображение в карточке продукта
                try:
                    image = k.find_element(By.TAG_NAME, 'img.product-card__image').get_attribute('src')
                except NoSuchElementException:
                    image = None
                name = k.find_element(By.CSS_SELECTOR, '.product-card__title').text
                price = k.find_element(By.CSS_SELECTOR, '.price-new').text
                add_new_product(name, 'Перекрёсток', price, type_of_product, image)


def main():
    url = 'https://www.perekrestok.ru/cat/'
    not_parsing_pages = [7, 14, 23, 24, 25, 26, 27, 29]
    parse_products(url, not_parsing_pages)


if __name__ == '__main__':
    main()
