# -*- coding: utf-8 -*-
import pandas as pd
from dateutil import parser
import requests
from django.core.management.base import BaseCommand, CommandError
# import
import json as js
# import models as mod
import os


CONFORMITY_DICT = {
    'BudgetReferenceBook': [
            'http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data',  # ! api_url
            '?pageSize=10',  # ! url api param
            {
                'code': ['code', 'code', ],
                'name': ['name', 'name', ],
                'parentcode': ['parentcode', 'parentcode', 'code'],
                'startdate': ['startdate', 'startdate', ],
                'enddate': ['enddate', 'enddate', ],
                'status': ['status', 'status', 'choices'],
                'budgettype': ['budgettype', 'budgtypecode', 'code']
            }
    ],
}
# ! Работа со словарем
# dct = CONFORMITY_DICT
# for modl in dct:
#     print(modl)
#     modl_name = modl
#     r = 0
#     for modl_att in dct[modl]:
#         print(r, modl_att)
#         r += 1
# for fld in dct[modl_name][1]:
#     print(dct[modl_name][1][fld])


class ImportDataFromAPI():
    """Класс импортирования данных из API и загрузки в модель."""

    def __init__(self, data_dict, model_name):
        self.data_dict = data_dict
        self.model_name = model_name

    def _get_field_type(field):
        """Возвращает тип поля модели"""
        try:
            field_type = field.get_iternal_type()
            return field_type
        except Exception:
            raise Exception("Error: it's not a field!!!")

    def _convert_value_fieldtype(field):
        """Передаем поле, получаем значение"""
        if not isinstance(field, str):
            raise Exception("Error: this field insn't correct!!!")
        else:
            field_type = self._get_field_type(field)
            if field_type == 'AutoField':
                field = int(field)
            elif (field_type == 'CharField') or (field_type == 'TextField'):
                if len(field) > field.max_length:
                    field = str(field)[:field.max_length]
                else:
                    field = str(field)
            elif field_type == 'DateTimeField':
                field = parser.parse(str(field))  # from 2019-05-02 22:16:28.0 to datetime.datetime(2019, 5, 2, 22, 16, 28)
            elif field_type == 'DateField':
                field = parser.parse(str(field)).date() # from 2019-05-02 to datetime.date(2019, 5, 2)
            elif (field_type == 'IntegerField') or (field_type == 'PositiveIntegerField'):
                field = int(field)
            elif (field_type == 'IntegerField'):
                pass

    def get_json_dict_from_api_url_response(self):
        """Возвращает json-словарь из request-объекта"""
        website_api = self.data_dict[self.model_name][0] + self.data_dict[self.model_name][1]
        if website_api is not None:
            try:
                request = requests.get(website_api)
                json_file = request.json()['data']
                json_file_len = len(json_file)
                if json_file_len > 0:
                    json_dict = {x: json_file[x] for x in range(0, len(json_file))}
                    json_dict = js.dumps(json_file)
                    return json_dict
                else:
                    raise Exception("Error: Empty data!!!")
            except Exception:
                raise Exception("Error: Empty data!!!")

    def get_model_field_types_list(self):
        app_label = 'task'  # * Имя приложения с моделями
        cur_model = models.get_model(app_label=app_label, model_name=self.model_name)  # * Получаем класс модели
        model_fields = cur_model._meta.local_fields  # * Получаем поля модели
        model_fields_list_len = len(model_fields)
        dict_fields = self.data_dict[self.model_name][2]
        for field_index in range(0, model_fields_list_len):
            # for 
            print(model_fields[field_index].name)

    def import_data_into_db(self):
        """Что нужно:
        app_label = 'task'  # * Имя приложения с моделями
        cur_model = models.get_model(app_label=app_label, model_name=self.model_name)  # * Получаем класс модели
        model_fields = cur_model._meta.local_fields  # * Получаем поля модели
        model_fields_list_len = len(model_fields)  # * 
        dict_fields = self.data_dict[self.model_name][2]
        """
        pass


class ImportFromAPI():
    """Класс импортирования модели из api стороннего web-сайта с помощью pandas"""

    def __init__(self, website_api, model_fields_list=None):
        self.website_api = website_api
        self.model_fields_list = model_fields_list

    # ! Получаем json из api url'а
    def get_json_from_api_url_response(self):
        """Возвращает json-словарь из request-объекта"""
        if self.website_api is not None:
            request = requests.get(self.website_api)
            json_file = request.json()
            return json_file
        else:
            raise Exception("Error: Incorrect website api url!!!")

    # ! Получаем df из json'а по ключу
    def get_pd_from_json_by_key(self, json_file, key):
        """Возвращает dataframe из словаря по ключу"""
        if (len(key) > 1) and (json_file is not None):
            dataframe = pd.DataFrame(json_file[key])
            return dataframe
        else:
            raise Exception("Error: Incorrect json or json's key!!!")

    # ! Получаем df по определенным полям
    def get_selected_fields_from_df(self, df, fields_list):
        """Возвращает dataframe с определенными полями"""
        if (len(fields_list) < 1) or (df is None):
            raise Exception("Error: Fields list is empty!!!")
        else:
            df_by_columns = df.loc[:, fields_list]
            return df_by_columns

    # ! Получаем df по определенным полям
    def get_model_fields_from_df(self, df):
        """Возвращает dataframe с определенными полями"""
        if (self.model_fields_list is None) or (df is None):
            raise Exception("Error: Fields list is empty!!!")
        else:
            df_by_columns = df.loc[:, self.model_fields_list]
            return df_by_columns


"""
Index(['guid', 'startdate', 'enddate', 'status', 'code', 'shortname',  
       'fullname', 'codesvr', 'codeasfk', 'codels', 'firstreqguid',    
       'firstreqnum', 'firstreqdate', 'lastreqguid', 'lastreqnum',     
       'lastreqdate', 'filenum', 'filedate', 'loaddate'],
      dtype='object')
"""


class ExportToModel():
    """Класс экспорта данных из dataframe в django model"""

    def __init__(self, model):
        self.model = self.model

    def get_object_manager(self):
        """Возвращает менеджер объектов модели"""
        if self.model is not None:
            object_manager = self.model.objects.all()
            return object_manager

    def get_model(self):
        """Получаем список полей модели"""
        pass


class Command(BaseCommand):
    help = 'Kek'

    def handle(self, *args, **kwargs):
        kek = ImportDataFromAPI(CONFORMITY_DICT, 'BudgetReferenceBook')
        json_dict = kek.get_json_dict_from_api_url_response()
        print(json_dict)
        # import this


# if __name__ == "__main__":
#     kek_class = ImportFromAPI(SPR_BUDG_API_URL)
#     my_json = kek_class.get_json_from_api_url_response()
#     print(len(my_json))
#     key = 'data'
#     df = pd.DataFrame(my_json[key])
#     # dataframe = kek_class.get_pd_from_json_by_key(json, key)
#     # print(dataframe)
#     print(df)


# if __name__ == "__main__":
#     kek = ImportDataFromAPI(CONFORMITY_DICT, 'BudgetReferenceBook')
#     json_dict = kek.get_json_dict_from_api_url_response()
#     print(json_dict)