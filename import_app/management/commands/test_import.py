# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from dateutil import parser
import requests
# import
import json as js
from django.apps import apps
import os

from ...apps import TaskConfig


APP_NAME = TaskConfig.name
CHOICE_VALUE_POSITION_IN_LIST = 0


CONFORMITY_DICT = {
    'Budget': {
        # 'url': 'http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data',
        # 'url_param': '?sortField=code&sortDir=asc&pageSize=65',
        'url': 'http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data',
        'url_param': '?sortField=parentcode&sortDir=asc',
        'fields': {
            'code': {'json_field_name': 'code'},
            'name': {'json_field_name': 'name'},
            # 'parentcode': ['parentcode', 'parentcode', 'code'],
            'parentcode': {'json_field_name': 'parentcode', 'to_field': 'code'},
            'startdate': {'json_field_name': 'startdate'},
            'enddate': {'json_field_name': 'enddate'},
            'status': {'json_field_name': 'status'},
            'budgettype': {'json_field_name': 'budgtypecode', 'to_field': 'code', 'to_model': 'BudgetType'}
        }
    },
    # 'GlavnRaspBudgetSred': {
    #     'url': 'http://budget.gov.ru/epbs/registry/7710568760-KBKGLAVA/data',
    #     'url_param': '?pageNum=2',
    #     'fields': {}
    # },
    # 'KodVedomstv': {
    #     'url': 'http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data',
    #     'url_param': '?pageNum=10',
    #     'fields': {}
    # },
}


class ImportDataFromAPI():
    """Класс импортирования данных из API и загрузки в модель."""

    # def __init__(self, data_dict):
    def __init__(self, data_dict, model_name):
        self.data_dict = data_dict
        self.model_name = model_name
        self.app_label = APP_NAME
        self.choice_val_position = CHOICE_VALUE_POSITION_IN_LIST

    # def __init__(self, data_dict):
    #     self.data_dict = data_dict

    def get_json_dicts_list_from_api_url(self):
        """Возвращает json-словарь из request-объекта."""

        url_name = self.data_dict[self.model_name]['url']
        url_param = self.data_dict[self.model_name]['url_param']
        website_api = url_name + url_param
        if website_api is not None:
            try:
                request = requests.get(website_api)  # * Отправляем http.get запрос
                json_data = request.json()['data']  # * Получаем json, поле data
                json_data_len = len(json_data)
                if json_data_len > 0:
                    json_dict = {x: json_data[x] for x in range(0, json_data_len)}
                    json_dict = js.dumps(json_data)
                    json_dict = js.loads(json_dict)
                    return json_dict
                else:
                    raise Exception("Error: Empty data!!!")
            except:
                raise Exception("Error: Empty data!!!")

    # def get_imported_values_dict(self, model_field, json_field):
    def get_imported_values_dict(self, json_dict):
        """Функция возвращает словарь значений для импорта."""

        # if (model_field is not None) and (json_field is not None):
        if (json_dict is None):
            raise Exception('Error: empty json!')
        cur_model = apps.get_model(app_label=self.app_label, model_name=self.model_name)  # * Получаем объект модели
        model_fields = cur_model._meta.local_fields[1:]  # * Список полей объекта модели - все без id
        ready_to_import_dict = {}  # * Словарь, в который будем отдавать данные
        for field in model_fields:  # * Перебираем поля модели
            field_name = field.name
            field_params = self.data_dict[self.model_name]['fields'][field_name]  # * Словарь параметров поля
            json_field_name = field_params['json_field_name']
            json_field_value = json_dict[json_field_name]  # * Значение поля json по значению из словаря
            field_type = field.get_internal_type()  # * Название типа поля(прим: TextField)
            if (field_type == 'TextField') or (field_type == 'CharField'):
                field_max_len = field.max_length  # * Получаем макс.длину поля модели
                json_field_value_len = len(json_field_value)  # * Получаем длину значения поля json
                choices = field.choices  # * Список принимаемых значений
                # ! Проверка для choice-полей
                if choices is not None:
                    for choice_list in choices:
                        if json_field_value == choice_list[self.choice_val_position]:
                            json_field = json_field_value
                            break
                        else:
                            json_field = None
                if (field_max_len is not None) and (json_field_value_len > field_max_len):
                    json_field = json_field_value[:field_max_len]  # * Обрезаем поле json до допустимой длины
                else:
                    json_field = json_field_value
            elif field_type == 'DateTimeField':
                json_field = parser.parse(str(json_field_value))  # * переводим из 2019-05-02 22:16:28.0 в datetime.datetime(2019, 5, 2, 22, 16, 28)
            elif field_type == 'DateField':
                json_field = parser.parse(str(json_field_value)).date()  # * переводим из 2019-05-02 в datetime.date(2019, 5, 2)
            elif field_type == 'ForeignKey':
                # * Для вторичного ключа, связанного с экземпляром другой модели
                if 'to_model' in field_params:
                    reference_model = apps.get_model(app_label=self.app_label, model_name=field_params['to_model'])
                else:
                    reference_model = cur_model
                queryset = reference_model.objects.all()
                query_get_param = {field_params['to_field']: json_field_value}  # * Название поля: значение
                queryset_val = queryset.get(**query_get_param)  # * Звездочка извлекает аргументы из структуры
                if queryset_val is not None:
                    json_field = queryset_val
                else:
                    if field.blank:
                        json_field = None
                    else:
                        raise Exception("Error: field cannot be empty but it is!")
            ready_to_import_dict[field_name] = json_field
        return ready_to_import_dict

    def import_to_model(self, json_dicts_list):
        """Импортирует словарь по 'поле': значение в модель."""
        if json_dicts_list is not None:
            cur_model = apps.get_model(app_label=self.app_label, model_name=self.model_name)  # * Получаем объект модели
            for row in json_dicts_list:
                row = self.get_imported_values_dict(row)
                if row is not None:
                    print('\n', row, '\n')
                    try:
                        cur_model.objects.create(**row)
                    except:
                        raise Exception('Error: import is failed!')
                else:
                    raise Exception(f'Error: The record: {row} with same is already exists!')
            return True
        else:
            raise Exception('Error: json list of dicts is empty!')


def importing():
    api_data = ImportDataFromAPI(CONFORMITY_DICT, 'Budget')
    json_data = api_data.get_json_dicts_list_from_api_url()
    # print(json_data)
    data = api_data.import_to_model(json_data)
    if data:
        return True
    return False
    # print(data)


class Command(BaseCommand):
    help = 'Импорт данных из url api в model'

    def handle(self, *args, **kwargs):
        return importing()
