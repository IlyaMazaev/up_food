from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from tqdm.auto import tqdm

from data import db_session  # db engine
from main_recipes_api import add_new_recipe


def setDriver():  # Запуск драйвера
    driver = webdriver.Chrome()
    return driver


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


def parse_recipes(product_url):  # Парсинг продуктов из категории
    db_session.global_init("../db/recipes_data.db")  # connecting to db

    driver = setDriver()
    recipe_url = get_all_recipes_card(product_url, driver)
    for i in tqdm(recipe_url):
        driver.get((i))  # Преход на страницу рецепта
        ingredients = list()
        name = driver.find_element(By.CLASS_NAME, 'css-gl52ge').text  # Получение названия
        product_list = driver.find_elements(By.CLASS_NAME, 'css-ipetvh-Column')  # Получение списка продуктов
        for j in product_list:
            ingredients.append(j.text)
        how_to_list = driver.find_element(By.CLASS_NAME, 'css-15qy3ai-composedStyles').find_elements(By.CLASS_NAME,
                                                                                                     'css-rc5iu8-Column')  # Получение инструкции
        types_list = driver.find_elements(By.CLASS_NAME, 'css-rit9g1-Info')  # Получение тэгов рецепта
        types = list()
        for j in types_list:
            types.append(j.text)
        how_to_cook = list()
        for j in how_to_list:
            how_to_cook.append(j.text)
        try:
            image = driver.find_element(By.CLASS_NAME, 'css-1b6pdfo-ImageBase').get_attribute(
                'src')  # Получение изображения
        except NoSuchElementException:
            image = None
        time = driver.find_element(By.CLASS_NAME, 'css-my9yfq').text  # Получение времени готовки
        portions = driver.find_element(By.XPATH,
                                       '//*[@id="__next"]/main/div/div/div/div/div[1]/div[2]/div[3]/div[1]/span[1]/span[2]/span').text  # Получение порции

        add_new_recipe(name, ';'.join(list(map(lambda x: ' - '.join(x.split('\n')), ingredients))), {'': ''},
                       ';'.join(how_to_cook), portions, time, ';'.join(types), image)
        print(name)


def main():
    url = 'https://eda.ru/recepty?page='
    parse_recipes(url)


if __name__ == '__main__':
    main()
