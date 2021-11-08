from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from tqdm.auto import tqdm

from data import db_session  # db engine
from main_recipes_api import add_new_product  # function from main_recipes_api


def add_parsed_data_from_perekrestok():
    db_session.global_init("../db/products.db")  # connecting to db

    product_pages = [113, 148]
    pages_counter = list()
    options = Options()
    options.add_argument("--headless")
    names_of_products = list()
    price_of_products = list()
    images_of_products = list()
    url = 'https://www.perekrestok.ru/cat/c/'
    webdriver = "chromedriver.exe"
    driver = Chrome(webdriver)
    for i in tqdm(range(0, len(product_pages))):
        product_url = url + str(product_pages[i]) + '/full?page='
        driver.get(product_url)
        element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "rc-pagination-item")))
        num_page = driver.find_elements_by_class_name('rc-pagination-item')
        pages_counter.append(num_page[len(num_page) - 1].text)
    for i in tqdm(range(0, len(product_pages))):
        for j in range(1, int(pages_counter[i]) + 1):
            if j == 1:
                product_url = url + str(product_pages[i]) + '/full?page='
            else:
                product_url = url + str(product_pages[i]) + '/full?page=' + str(j)
            driver.get(product_url)
            element = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "product-card__link-text")))
            name = driver.find_elements_by_class_name('product-card__link-text')
            price = driver.find_elements_by_class_name('price-new')
            image = driver.find_elements_by_class_name('product-card__image')
            for k in range(0, len(name)):
                names_of_products.append(name[k].text)
            for k in range(0, len(price)):
                price_of_products.append(price[k].text)
            for k in image:
                images_of_products.append(k.get_attribute('src'))

        for name, price, photo in zip(names_of_products, price_of_products, images_of_products):
            add_new_product(name, 'Перекрёсток', price, photo)


def main():
    add_parsed_data_from_perekrestok()


if __name__ == '__main__':
    main()
