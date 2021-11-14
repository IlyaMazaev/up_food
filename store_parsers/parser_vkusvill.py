from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from tqdm.auto import tqdm

from data import db_session  # db engine
from main_recipes_api import add_new_product  # function from main_recipes_api


def add_parsed_data_from_vkusvill():
    db_session.global_init("../db/recipes_data.db")  # connecting to db

    pages_counter = list()
    options = Options()
    options.add_argument("--headless")
    names_of_products = list()
    price_of_products = list()
    images_of_products = list()
    url = 'https://vkusvill.ru/goods/supermarket/?PAGEN_1='
    webdriver = "chromedriver.exe"
    driver = Chrome(webdriver)
    for i in tqdm(range(0, 247)):
        product_url = url + str(i)
        driver.get(product_url)
        name = driver.find_elements_by_class_name('ProductCard__link')
        price = driver.find_elements_by_class_name('Price__value')
        image = driver.find_elements_by_class_name('ProductCard__imageImg')
        for k in range(0, len(name)):
            names_of_products.append(name[k].text)
        for k in range(0, len(price)):
            price_of_products.append(price[k].text)
        for k in image:
            images_of_products.append(k.get_attribute('src'))

    for name, price, photo in zip(names_of_products, price_of_products, images_of_products):
        add_new_product(name, 'Вкусвилл', price, photo)


def main():
    add_parsed_data_from_vkusvill()


if __name__ == '__main__':
    main()
