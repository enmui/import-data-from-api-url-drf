from django.core.management.base import BaseCommand
import requests
from ...serializers import BudgetSerializer


def get_data_from_api(url):
    """Возвращает список объектов json."""
    try:
        request = requests.get(url)  # * Отправляем http.get запрос
        json_data = request.json()['data']  # * Получаем json, поле data
        json_data_len = len(json_data)
        if json_data_len > 0:  # * В случае выполнения
            return json_data
        else:
            raise Exception("Error: Empty data!!!")
    except:
        raise Exception("Error: Invalid url!!!")


def deserialize_data_from_json(json, serializer_class):
    """"Дессереализация данных из json в BudgetSerializer"""
    for record in json:  # * обход записей json'аs
        serialized_data = serializer_class(data=record)
        if serialized_data.is_valid():  # * raise_exception=True - поднимать exception
            serialized_data.save()
        else:
            print('\n', f'Ошибка валидации: {serialized_data.errors}', '\n', f'Строка: {record}')


def make_import():
    """Выполняет импорт данных со стороннего api в модель."""
    url_str = 'http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data?pageNum=100'  # * Запрос к api
    json_data = get_data_from_api(url_str)  # * Получаем данные json из api по url_str
    serializer_class = BudgetSerializer  # * Класс сериализатора
    deserialize_data_from_json(json_data, serializer_class)  # * Выполняем дессериализацию и импорт


class Command(BaseCommand):
    help = 'Тест работы сериализатора'
    def handle(self, *args, **kwargs):
        import_ = make_import()
        return import_
