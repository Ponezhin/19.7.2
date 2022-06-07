from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# Блок тестов на получение api ключа

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

def test_get_api_key_for_non_password_user(email=valid_email, password=''):
    """ Проверяем, что при отсутствии данных в поле password, запрос возвращает код ошибки 403,
     а так же в результате отсутствует слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_non_email_user(email='', password=valid_password):
    """ Проверяем, что при отсутствии данных в поле email, запрос возвращает код ошибки 403,
     а так же в результате отсутствует слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_non_valid_user(email='Gbgdgn@gsgl.com', password='Dv%f;dGew435'):
    """ Проверяем, что запрос возвращает код ошибки 403, означающий,
    что комбинация логина и пароля неверна, а так же нет слова key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


# Блок тестов на проверку списка питомцев

def test_get_all_pets_with_valid_key(filter=''):
    """Позитивный тест получения не пустого списка питомцев по фильтру 'Все питомцы'.
    Сначала получаем API ключ.
    После поверяем, что запрос возвращает статус 200 и список питомцев не пустой (фильтр 'Все питомцы')"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_get_my_pets_with_valid_key(filter='my_pets'):
    """Позитивный тест получения не пустого списка питомцев по фильтру 'Мои питомцы'. Получаем API ключ.
    После поверяем, что запрос возвращает статус 200 и список питомцев не пустой (фильтр 'Мои питомцы')"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    if len(result['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'Котейка', 'Британец', '9')
        # Еще раз запрашиваем список моих питомцев
        status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_non_valid_key(filter=''):
    """Тест получения списка питомцев по фильтру 'Все питомцы' при невалидном API ключе.
    Проверяем, что запрос возвращает статус 403 и в тексте ответа есть слово Forbidden"""

    auth_key = {'key': 'k123456456789sa34445dltd'}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'Forbidden' in result


# Блок тестов на проверку добавления питомцев

def test_add_new_pet_with_valid_data(name='Кроль', animal_type='кролик', age='3', pet_photo='image/krol.jpg'):
    """Позитивный тест добавления нового питомца с корректными данными.
    Получаем полный путь изображения питомца и сохраняем в переменную pet_photo.
    Запрашиваем ключ api и сохраняем в переменную auth_key и добавляем питомца.
    Сверяем полученный ответ с ожидаемым результатом"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_non_valid_key(name='Кроль', animal_type='кролик', age='3', pet_photo='image/krol.jpg'):
    """Тест добавления нового питомца с некорректным ключом.
    Получаем полный путь изображения питомца и сохраняем в переменную pet_photo.
    Добавляем некорректный ключ api и сохраняем в переменную auth_key. Добавляем питомца.
    Проверяем что возвращается статус 403 и в тексте ответа есть слово Forbidden """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key = {'key': 'k123456456789sa34445dltd'}
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert 'Forbidden' in result

def test_add_new_pet_with_empty_data(name='', animal_type='', age='', pet_photo='image/oslic.jpg'):
    """Тест добавления нового питомца только с фото без заполненных данных name, animal_type, age.
    Получаем полный путь изображения питомца и сохраняем в переменную pet_photo.
    Запрашиваем ключ api и сохраняем в переменную auth_key. Добавляем питомца.
    Проверяем, что возвращается статус 200 и в результате ответа нет имени."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == ''

def test_add_new_pet_with_valid_data_no_foto(name='Кроль', animal_type='кролик', age='3'):
    """Тест добавления нового питомца с корректными данными name, animal_type, age и без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet_no_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_foto_pet_with_valid_data(pet_photo='image/oslic.jpg'):
    """Тест добавления фото питомца с корректными данными"""


    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'Иа', 'Ослик', '9')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_add_photo_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['id'] == pet_id



# Блок тестов на проверку удаления питомцев

def test_successful_delete_self_pet():
    """Позитивный тест удаления питомца. Получаем ключ auth_key и запрашиваем список своих питомцев.
    Берём id первого питомца из списка и отправляем запрос на удаление.
    Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'Иа', 'Ослик', '9', 'image/oslic.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_pet_non_correct_key():
    """Тест удаления питомца с некорректным ключом.
    Получаем рабочий ключ auth_key и запрашиваем список своих питомцев.
    Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев.
    Берём id первого питомца из списка и некорректный ключ auth_key_false и делаем запрос на удаление.
    Проверяем что статус ответа равен 403 и в результате есть Forbidden.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'Иа', 'Ослик', '9', 'image/oslic.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    auth_key_false = {'key': 'ksa312345678944ldld'}
    status, result = pf.delete_pet(auth_key_false, pet_id)

    assert status == 403
    assert 'Forbidden' in result

def test_delete_pet_non_correct_id():
    """Негативный тест удаления питомца с некорректным ID. Получаем рабочий ключ auth_key.
    Берём некорректный id и ключ auth_key и делаем запрос на удаление.
    Проверяем что статус ответа равен 404 и в результате есть Not Found.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = ''
    status, result = pf.delete_pet(auth_key, pet_id)

    assert status == 404
    assert 'Not Found' in result

# Блок тестов на проверку обновления данных питомцев

def test_successful_update_self_pet_info(name='Матюсище', animal_type='двортерьер', age=6):
    """Позитивный тест успешного обновления информации о питомце.
    Проверяем что статус ответа = 200 и имя питомца соответствует заданному"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    else:
        pf.post_add_new_pet(auth_key, 'Кроль', 'Кролик', '3', 'image/krol.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        status, result = pf.put_update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_update_pet_info_non_correct_key(name='Матюсище', animal_type='двортерьер', age=6):
    """Негативный тест обновления информации о питомце с некорректным ключом.
    Проверяем что статус ответа = 403 и в результате есть Forbidden"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    auth_key_false = {'key': 'k123456789sa344ldld'}

    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key_false, my_pets['pets'][0]['id'], name, animal_type, age)
    else:
        pf.post_add_new_pet(auth_key, 'Кроль', 'Кролик', '3', 'image/krol.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        status, result = pf.put_update_pet_info(auth_key_false, my_pets['pets'][0]['id'], name, animal_type, age)

    assert status == 403
    assert 'Forbidden' in result
