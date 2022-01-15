from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from tqdm.auto import tqdm

from data import db_session  # db engine

from main import add_new_product


def setDriver():  # Запуск драйвера
    driver = webdriver.Chrome()
    return driver


def check_numbers_of_pages(url, driver):  # Нахождение количества страниц в категории
    element = WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '.lk-pager.js-lk-pager')))  # Проверка загрузилась ли страницы
    numbers_of_pages = (driver.find_element(By.XPATH, '//*[@id="section_lvl2"]/div[25]/footer/div/a[6]').text)
    return numbers_of_pages


def parse_products_vkusvill(product_url, not_parsing_pages):  # Парсинг продуктов из категории
    db_session.global_init("../db/products_data.db")  # connecting to db

    driver = setDriver()
    driver.get(product_url)
    product_list = list()
    url_list = list()
    elements_of_types_of_food = driver.find_elements(By.CLASS_NAME, 'VVCategCards2020__Col')  # Поиск всех категорий
    for i in tqdm(range(0, len(elements_of_types_of_food))):
        url_list.append(elements_of_types_of_food[i].find_element(By.TAG_NAME, 'a').get_attribute('href'))
    for i in tqdm(range(4, len(url_list))):
        if i in not_parsing_pages:
            continue
        driver.get(url_list[i])
        element = WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '.ProductCard__imageImg.lazyload')))  # Проверка загрузилась ли страницы
        max_page_number = check_numbers_of_pages(driver.current_url, driver)  # Поиск страниц
        url = driver.current_url + '?PAGEN_1='
        for j in range(1, int(max_page_number) + 1):
            driver.get(url + str(j))
            element = WebDriverWait(driver, 10).until(
                ec.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, '.ProductCard__imageImg.lazyload')))  # Проверка на загруженность страницы
            product_card = driver.find_elements(By.CLASS_NAME,
                                                'ProductCards__item')  # Поиск карточки продукта и названия категории
            type_of_product = driver.find_element(By.CLASS_NAME, 'VVCatalog2020SectH1').text
            for k in product_card:  # Поиск названия, цены, ссылки на изображение в карточке продукта
                image = k.find_element(By.CSS_SELECTOR, '.ProductCard__imageImg.lazyload').get_attribute('src')
                name = k.find_element(By.CLASS_NAME, 'ProductCard__link').text
                price = k.find_element(By.CLASS_NAME, 'Price__value').text
                add_new_product(name, 'Вкусвилл', price, type_of_product, image)


def main():
    url = 'https://vkusvill.ru/goods/'
    not_parsing_pages = [7, 8, 9, 24, 25, 26, 27, 28, 30]
    parse_products_vkusvill(url, not_parsing_pages)


if __name__ == '__main__':
    main()
