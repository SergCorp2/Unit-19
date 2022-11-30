import os.path

from app.api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
#    assert  status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Мыш', animal_type='дворянин',
                                     age='2', pet_photo='images/1.jpg'):
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

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мышь", "дворянин", "2", "images/1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


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
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии
        # своих питомцев
        raise Exception("There is no my pets")




#"""" Тесты для задания 19.7.2"""



def test_add_new_pet_simple(name='Кыш', animal_type='кот', age='2'):
    """Проверяем что можно добавить питомца с верными данными но без фото"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name



def test_add_new_uncorrect_age_pet_simple(name='Кыш', animal_type='кот', age='-2'):
    """Проверяем, что можно добавить питомца с  не верными данными,
    отрицательным значением возраста"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name




def test_add_new_pet_simple_empty(name='', animal_type='', age=''):
    """Проверяем, что можно добавить питомца с пустыми данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name




def test_add_new_uncorrect_pet_simple(name='15', animal_type='22', age='кот'):
    """Проверяем, что можно добавить питомца с цифрами в имени и породе и
    буквенными данными в возрасте"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name



def test_add_photo_of_pet(pet_photo='images/2.jpg'):
    """Проверяем возможнотсь добавления фото к карточке питомца"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200 и в фото не пустое
        assert status == 200
        assert result['pet_photo'] is not None
    else:
        raise Exception("There is no my pets")




def test_add_not_photo_of_pet(pet_photo='images/3.txt'):
    """Проверяем возможнотсь добавления файла содержащего не фото к карточке питомца"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 500
    else:
        raise Exception("There is no my pets")



def test_successful_update_self_pet_broken_info(name='123', animal_type='321', age=5):
    """Проверяем возможность обновления информации о питомце, вместо имени и породы
    введем цифры"""

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
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии
        # своих питомцев
        raise Exception("There is no my pets")




def test_get_api_key_for_invalid_user_email(email='ghffhcg', password=valid_password):
    """Проверяем, что доступ к сайту не будет открыт при неверной почте """
    status, result = pf.get_api_key(email, password)
    assert status == 403



def test_get_api_key_for_invalid_user_password(email=valid_email, password='13546545'):
    """Проверяем, что доступ к сайту не будет открыт при неверной пароле """
    status, result = pf.get_api_key(email, password)
    assert status == 403



def test_get_api_key_for_invalid_user(email='', password=''):
    """Проверяем, что доступ к сайту не будет открыт при незаполнении данных """
    status, result = pf.get_api_key(email, password)
    assert status == 403



