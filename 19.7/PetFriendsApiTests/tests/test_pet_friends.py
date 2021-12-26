from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

"""Позитивное тестирование"""

# тест на получение api ключа с валидными данными
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

# тест на получение списка питомцев с валидным ключом
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

# тест на добавление питомца с валидными данными
def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# тест на удаление питомца
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

# тест на обновление данных о питомце
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# тест на добавление питомца без фотографии
def test_successful_add_information_about_new_pet_without_photo(name='Иваныч', animal_type='Песик', age='12'):
    """Проверяем возможность добавления питомца с корректными данными без фотографии"""

    # Запрашивем ключ auth_key и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# тест на добавление фото последнему питомцу в списке "Мои питомцы"
def test_successful_add_photo_of_pet(pet_photo='images/unnamed.jpg'):
    """Проверяем возможность добавления фото питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашивем ключ auth_key и сохраняем в переменную auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Иваныч", "Песик", "12")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берем id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']
    name = my_pets['pets'][0]['name']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

"""Негативное тестирование"""

# тест на не получение api ключа с невалидными данными
def test_negative_get_api_key(email=valid_email, password='1234567890'):
    """Проверяем, что запрос возвращает ошибку при недействительных данных"""
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями (статус не 200)
    assert status != 200
    assert 'key' not in result

# тест на не получение списка питомцев с невалидным ключом
def test_negative_get_all_pets_with_not_valid_key(filter=''):
    """Проверяем, что запрос возвращает ошибку при недействительном ключе"""
    auth_key = {'key': '1234567890'}
    status, result = pf.get_list_of_pets(auth_key, filter)

    error_message = "Please provide 'auth_key' Header"
    # Сверяем полученные данные с нашими ожиданиями
    assert status != 200
    assert error_message in result

# тест на не добавление питомца с невалидным ключом
def test_negative_add_new_pet_with_not_valid_key(name='Иваныч', animal_type='Песик',
                                                  age='12', pet_photo='images/unnamed.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = {'key': '1234567890'}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Создаем переменную с нужной нам ошибкой
    error_message = "Please provide 'auth_key' Header"
    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert error_message in result

# тест на не удаление питомца с невалидным ключом
def test_negative_delete_self_pet_with_not_valid_key():
    """Проверяем возможность не удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    # Создаем невалидный ключ
    auth_key_not_valid = {'key': '1234567890'}
    status, _ = pf.delete_pet(auth_key_not_valid, pet_id)

    # Проверяем что статус ответа не равен 200
    assert status != 200

# тест на не обновление данных о питомце с невалидным ключом
def test_negitaive_update_self_pet_info_with_not_valid_key(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Создаем невалидный ключ
    auth_key_not_valid = {'key': '1234567890'}
    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key_not_valid, my_pets['pets'][0]['id'], name, animal_type, age)
        # Создаем переменную с нужной нам ошибкой
        error_message = "Please provide 'auth_key' Header"
        # Проверяем что статус ответа != 200 и в результате выводится ошибка
        assert status != 200
        assert error_message in result
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# тест на не добавление фото последнему питомцу в списке "Мои питомцы" с невалидным ключом
def test_negative_add_photo_of_pet_with_not_valid_key(pet_photo='images/unnamed.jpg'):
    """Проверяем возможность не добавления фото питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашивем ключ auth_key и сохраняем в переменную auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Иваныч", "Песик", "12")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Создаем невалидный ключ
    auth_key_not_valid = {'key': '1234567890'}
    # Создаем переменную с нужной нам ошибкой
    error_message = "Please provide 'auth_key' Header"
    # Берем id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']
    name = my_pets['pets'][0]['name']
    status, result = pf.add_photo_of_pet(auth_key_not_valid, pet_id, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert error_message in result

# тест на не добавление питомца без фотографии с невалидным ключом
def test_negative_add_information_about_new_pet_without_photo_with_not_valid_key(name='Иваныч',
                                                                                 animal_type='Песик', age='12'):
    """Проверяем возможность не добавления питомца без фотографии"""

    # Запрашивем ключ auth_key и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Создаем невалидный ключ
    auth_key_not_valid = {'key': '1234567890'}
    # Создаем переменную с нужной нам ошибкой
    error_message = "Please provide 'auth_key' Header"
    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key_not_valid, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert error_message in result

# тест на не добавление питомца без фотографии с пустыми данными
def test_negative_add_information_about_new_pet_without_photo_with_empty_data(name='', animal_type='', age=''):
    """Проверяем возможность не добавления питомца с пустыми данными без фотографии"""

    # Запрашивем ключ auth_key и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert result['name'] != name