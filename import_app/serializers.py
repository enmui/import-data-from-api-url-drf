from rest_framework import serializers
from .custom_serializers import ModelMappingSerializer
from . import models


class BudgetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Budget"""

    code = serializers.CharField(max_length=8, allow_null=False)
    name = serializers.CharField(max_length=2000, allow_null=False)
    startdate = serializers.DateTimeField(allow_null=False)
    enddate = serializers.DateTimeField(allow_null=True)
    status = serializers.ChoiceField(choices=models.KBKStatus.choices, allow_null=False)
    parentcode = serializers.PrimaryKeyRelatedField(queryset=models.Budget.objects.all(), allow_null=True, required=False)
    budgtypecode = serializers.PrimaryKeyRelatedField(source='budgettype', queryset=models.BudgetType.objects.all(), allow_null=True, required=False)

    class Meta:
        model = models.Budget
        fields_mapping = {
            'parentcode': {'json_field_name': 'parentcode', 'to_field': 'code'},
            'budgettype': {'json_field_name': 'budgtypecode', 'to_field': 'code', 'to_model': models.BudgetType}
        }

        fields = '__all__'

    def create(self, validated_data):
        try:
            instance = self.Meta.model.objects.create(**validated_data)
            return instance
        except TypeError:
            raise TypeError("Error: Can't create the record!")

    def to_internal_value(self, data):
        for data_key in data:
            if data[data_key] == '':
                data[data_key] = None  # ! Это нужно для того, чтобы не проходила пустая строка даты

        fields_mapping = self.Meta.fields_mapping

        for field in fields_mapping:  # ! Обходим каждое 'поле' fields_mapping словаря

            if data[fields_mapping[field]['json_field_name']] is None:  # ! Если ссылочное поле имеет пустое значение - это нормально, пропускаем итерацию - переходим к другому полю
                continue

            to_field = fields_mapping[field]['to_field']

            if to_field is not None:  # ! Проверка наличия ключа поля, по значению которого будем искать ссылку
                queryset_param = {to_field: data[fields_mapping[field]['json_field_name']]}  # ! Параметр, который передается в запрос 'queryset_param=data_field_value'

                if 'to_model' in fields_mapping[field]:  # ! Проверка наличия ключа модели, к объектному менеджеру которой выполняется запрос
                    model = fields_mapping[field]['to_model']
                else:
                    model = self.Meta.model  # ! Если поле ссылается на объект этой же модели

                try:
                    queryset = model.objects.get(**queryset_param)  # ! get возвращает объект результирующего запроса или поднимает exception
                except:
                    queryset = None  # ! Нужна для нижней проверки - без объявления нельзя

                if queryset:  # ! Если запрос возвращает пустой результат
                    data[fields_mapping[field]['json_field_name']] = queryset.pk  # ! ссылочное поле ссылается по идентификатору

        return super().to_internal_value(data)
