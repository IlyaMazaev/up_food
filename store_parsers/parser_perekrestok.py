from selenium import webdriver
from selenium.webdriver.common.by import By


def setDriver():  # Запуск драйвера
    driver = webdriver.Chrome()
    return driver


class Product:
    def __init__(self, name, price, image, type_of_product):
        self.name = name
        self.price = price
        self.image = image
        self.type = type_of_product


def parse_products(product_url, not_parsing_pages):  # Парсинг продуктов из категории
    driver = setDriver()
    driver.get(product_url)
    product_list = list()
    elements_of_types_of_food = driver.find_element(By.CSS_SELECTOR, '.catalog__list').find_elements(By.CSS_SELECTOR,
                                                                                                     'div.category-card__title')  # Поиск всех категорий
    for i in range(4, len(elements_of_types_of_food)):
        if i in not_parsing_pages:
            continue
        elements_of_types_of_food[i].click()
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
                image = k.find_element(By.TAG_NAME, 'img.product-card__image').get_attribute('src')
                name = k.find_element(By.CSS_SELECTOR, '.product-card__title').text
                price = k.find_element(By.CSS_SELECTOR, '.price-new').text
                product_list.append(Product(name, price, image, type_of_product))
    return product_list


product_list = list()
url = 'https://www.perekrestok.ru/cat/'
not_parsing_pages = [7, 14, 23, 24, 25, 26, 27, 29]
product_list = parse_products(url, not_parsing_pages)
