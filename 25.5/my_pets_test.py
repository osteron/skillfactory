from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.wait import WebDriverWait

from config import *


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome(".\chromedriver\chromedriver.exe")
    # Переходим на страницу аутентификации
    pytest.driver.get(URL_LOGIN)

    yield

    pytest.driver.quit()


def test_show_all_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(EMAIL)
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(PASSWORD)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Неявное ожидание всех элементов (фото, имя питомца, его возраст)
    pytest.driver.implicitly_wait(10)

    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(EMAIL)
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(PASSWORD)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку навигации с явным ожиданием
    WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "navbar-toggler-icon"))).click()
    # Нажимаем на кнопку "Мои питомцы" с явным ожиданием
    WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Мои питомцы"))).click()
    # Проверяем URL
    assert pytest.driver.current_url == URL_MY_PETS
    # Ожидаем отображение таблицы питомцев
    WebDriverWait(pytest.driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='all_my_pets']/table")))
    # Находим строки с питомцами = количество питомцев
    pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Сравниваем количество найденных питомцев с итоговым значением
    assert len(pets) == COUNT_OF_PETS
    # Берем фотографии
    images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    # Берем имена животных
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    # Берем породы животных
    breed = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    # Берем возраст животных
    age = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    # Список значений src для фотографий питомцев
    list_src_images = []
    # Переменная для подсчета количества не пустых фотографий
    count_of_images = 0
    # Список подсчета уникальных имен
    unique_names = []
    # Список подсчета уникальных питомцев
    unique_pets = []
    # Цикл по количеству питомцев
    for i in range(len(pets)):
        # Считаем количество не пустых фотографий
        if images[i].get_attribute('src') != '':
            count_of_images += 1
        # Добавляем значение src фотографии питомца в список
        list_src_images.append(images[i].get_attribute('src'))
        # Проверяем имя на не пустое значение
        assert names[i].text != ''
        # Добавляем имя питомца в список
        unique_names.append(names[i].text)
        # Проверяем породу на не пустое значение
        assert breed[i].text != ''
        # Проверяем возраст на не пустое значение
        assert age[i].text != ''
        # Повторяющиеся питомцы (конкатенация src_img, имени, породы и возраста)
        unique_pets.append(list_src_images[i] + names[i].text + breed[i].text + age[i].text)
    # Сравниваем количество не пустых фотографий с (количество питомцев / 2)
    assert count_of_images >= (len(pets) / 2)
    # Проверяем уникальность имен питомцев
    assert len(pets) == len(set(unique_names))
    # Проверяем уникальность питомцев по всем четырем пунктам (фото, имя, порода и возраст)
    assert len(pets) == len(set(unique_pets))
