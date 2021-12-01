from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from tqdm import tqdm


def setDriver():  # Запуск драйвера
    driver = webdriver.Chrome()
    return driver


class Recipe:
    def __init__(self, name, image, products, how, portions, time, types):
        self.name = name
        self.products = products
        self.image = image
        self.how = how
        self.portions = portions
        self.time = time
        self.types = types


def get_all_recipes_card(product_url, driver):
    for i in tqdm(range(1, 200)):
        driver.get(product_url + str(i))  # Проход по всем страницам сайта
        try:
            recipes_cards = driver.find_elements(By.CLASS_NAME, 'css-10q2glf-Column')
        except NoSuchElementException:
            break
        recipe_url = list()
        for j in recipes_cards:
            recipe_url.append(j.find_element(By.TAG_NAME, 'a').get_attribute('href'))  # Сохранение ссылок на рецепты
    return recipe_url


def parse_products(product_url):  # Парсинг продуктов из категории
    recipe_list = list()
    driver = setDriver()
    recipe_url = get_all_recipes_card(product_url, driver)
    for i in tqdm(recipe_url):
        driver.get((i))  # Преход на страницу рецепта
        products = list()
        name = driver.find_element(By.CLASS_NAME, 'css-gl52ge').text  # Получение названия
        product_list = driver.find_elements(By.CLASS_NAME, 'css-ipetvh-Column')  # Получение списка продуктов
        for j in product_list:
            products.append(j.text)
        how_to_list = driver.find_element(By.CLASS_NAME, 'css-15qy3ai-composedStyles').find_elements(By.CLASS_NAME,
                                                                                                     'css-rc5iu8-Column')  # Получение инструкции
        types_list = driver.find_elements(By.CLASS_NAME, 'css-rit9g1-Info')  # Получение тэгов рецепта
        types = list()
        for j in types_list:
            types.append(j.text)
        how = list()
        for j in how_to_list:
            how.append(j.text)
        try:
            image = driver.find_element(By.CLASS_NAME, 'css-1b6pdfo-ImageBase').get_attribute(
                'src')  # Получение изображения
        except NoSuchElementException:
            image = None
        time = driver.find_element(By.CLASS_NAME, 'css-my9yfq').text  # Получение времени готовки
        portions = driver.find_element(By.XPATH,
                                       '//*[@id="__next"]/main/div/div/div/div/div[1]/div[2]/div[3]/div[1]/span[1]/span[2]/span').text  # Получение порции
        recipe_list.append(Recipe(name, image, products, how, portions, time, types))
        print(name)
    return recipe_list


recipe_list = list()
url = 'https://eda.ru/recepty?page='
recipe_list = parse_products(url)
