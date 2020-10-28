from django.core.management.base import BaseCommand
import requests
from ...serializers import BudgetSerializer


# ! Где ошибка
def make_import():
    # url = 'http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data?pageSize=81854&filterstatus=ACTIVE'
    url = 'http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data?pageSize=1000&filterstatus=ACTIVE&pageNum=1'
    serializer_class = BudgetSerializer  # * Класс сериализатора
    request = requests.get(url)  # * Отправляем http.get запрос
    page_count = int(request.json()['pageCount'])  # ! Кол-во страниц при текущей пагинации
    json_data = None
    for pagenum in range(1, (page_count + 1)):  # ! +1 - потому, что "число до" не включется в числовую послеовательность
        pagenum_param_str = 'pageNum='  # * Параметр номера страницы
        param_pos = url.find(pagenum_param_str)  # * Находим параметр в строке запроса api
        url = url[:param_pos] + (pagenum_param_str + str(pagenum))  # * Заменяем параметр в строке запроса api - устанавливаем номер страницы
        request = requests.get(url)  # * Отправляем http.get запрос
        if json_data is not None:  # ! Если с импорта предыдущей стриницы остались незагруженные, то:
            json_data = request.json()['data'] + json_data  # ! помещаем их в конец списка с новыми данными
        else:
            json_data = request.json()['data']  # * Получаем json, поле data
        not_imported_preview = 1 # * Кол-во незагр. на пред. шаге
        not_imported = 0  # * Кол-во незагруженных на текущем шаге
        not_imported_json = []  # * Список незаруженных данных
        while (not_imported_preview > 0) and (not_imported != not_imported_preview):  # ! Пока кол-во незагруженных > 0 и кол-во незагруже
            count_to_import = len(json_data)
            for record in json_data:  # * обход записей json'а
                current_record = record
                # ! Ссылочные поля не должны быть пустыми
                serialized_data = serializer_class(data=record)

                if serialized_data.is_valid():  # * raise_exception=True - поднимать exception
                    serialized_data.save()
                else:
                    # ! Сохраняем запись в отдельный json-file, увеличиваем счетчик ошибок +1
                    not_imported_json.append(current_record)
                    not_imported += 1
            if count_to_import <= not_imported:
                return None
                # break
            json_data = not_imported_json
            not_imported_preview = not_imported
            not_imported = 0


class Command(BaseCommand):
    help = 'Тест работы сериализатора'

    def handle(self, *args, **kwargs):
        import_ = make_import()
        return import_
