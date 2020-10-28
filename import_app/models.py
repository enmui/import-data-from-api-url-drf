from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as description
import uuid
import datetime


# Create your models here.
# # ! Информация откуда взята модель
# class ModelSourceInfo(models.Model):
#     """Описание модели Инофрмация о модели"""

#     model_name =    models.CharField("Имя модели", max_length=255, blank=False, null=False)
#     source_file =   models.FileField("Файл с информацией", upload_to='uploaded_files/%Y/%m/%d/')
#     source_url =    models.URLField("Url с информацией", max_length=200)
#     comment =       models.TextField("Комментарий")

#     class Meta:
#         verbose_name = 'Информация о модели'
#         verbose_name_plural = 'Информация о моделях'

#     # def clean(self):
#     #     super().clean()
#     #     if self.source_file is None and self.source_url is None:
#     #         raise ValidationError('Fields source_file and source_ulr are both None!!!')

#     def save(self, *args, **kwargs):
#         all_values = [self.source_file, self.source_url]
#         not_null_values = [val for val in all_values if val]
#         if len(not_null_values) > 0:
#             super(ModelSourceInfo, self).save(*args, **kwargs)
#         else:
#             raise ValidationError('Fields source_file and source_ulr are both None!!!')


# ! Классификаторы
class NPA(models.Model):
    """Описание модели Нормативно-правовой акт."""

    # TODO: Define fields here
    namenpa         = models.TextField("Наименование", max_length=2000, blank=False, null=False)
    numbernpa       = models.TextField("Номер", max_length=127)
    approvaldate    = models.DateTimeField("Дата утверждения")
    npaagency       = models.TextField("Код единицы измерения по ОКЕИ", max_length=2000)
    npakind         = models.TextField("Вид нормативно-правового акта", max_length=127)
    startdate       = models.DateTimeField("Дата вступления в силу")
    denotation      = models.TextField("Информация о статье, части, пункте", max_length=2000)

    class Meta:
        """Описание метакласса Нормативно-правовой акт."""

        verbose_name = 'Нормативно-правовой акт'
        verbose_name_plural = 'Нормативно-правовые акты'

    def __str__(self):
        """Строковое представление Нормативно-правовой акт."""
        return f"{self.nambernpa}: {self.namenpa}"


class PPO(models.Model):
    """Описание модели Публично-правовое образование."""

    # TODO: Define fields here
    code            = models.CharField("Код", max_length=3, blank=False, null=False)
    name            = models.TextField("Наименование", max_length=127, blank=False, null=False)
    constr          = models.TextField("Ограничение", max_length=2000)
    npa             = models.ForeignKey(NPA, verbose_name="Нормативно-правовой акт", blank=False, null=False, on_delete=models.CASCADE)

    class Meta:
        """Описание метакласса Публично-правовое образование."""
        verbose_name = "Публично-правовое образование"
        verbose_name_plural = "Публично-правовые образования"

    def __str__(self):
        """Строковое представление Публично-правовое образование."""
        return f"{self.code}: {self.name}"


# * --- Добавлено 29.09.2020 ---
# ! КБК/Главы -- статусы
class KBKStatus(models.TextChoices):
    """Уровень бюджета"""
    ACTIVE = "ACTIVE", description('Актуальная запись')
    ARCHIVE = "ARCHIVE", description('Архивная запись')


# ! Тофк
class TOFK(models.Model):
    """Описание модели Территориальный орган федерального казначейства. ТОФК."""

    # TODO: Define fields here
    guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36, blank=False, null=False, default='', validators=[MinLengthValidator(36)])
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    enddate             = models.DateTimeField("Дата окончания действия записи")
    status              = models.CharField("Статус записи", max_length=7, choices=KBKStatus.choices, blank=False, null=False)
    code                = models.CharField("Код", max_length=4, blank=False, null=False, unique=True)
    shortname           = models.TextField("Сокращенное наименование", max_length=254)
    fullname            = models.TextField("Полное наименование", max_length=2000, blank=False, null=False)
    inn                 = models.CharField("ИНН", max_length=10, blank=False, null=False)
    kpp                 = models.CharField("КПП", max_length=9, blank=False, null=False)
    addresslegal        = models.TextField("Юридический адрес", max_length=1000)
    tofkcode            = models.CharField("ТОФК (где введен)", max_length=4, blank=False, null=False)
    opendate            = models.DateTimeField("Дата создания ОрФК", blank=False, null=False, default=datetime.datetime.now)
    closedate           = models.DateTimeField("Дата ликвидации ОрФК")
    loaddate            = models.DateTimeField("Дата загрузки на ЕПБС", blank=False, null=False, default=datetime.datetime.now)
    filedate            = models.DateTimeField("Дата файла, дата выгрузки из сводного реестра", blank=False, null=False, default=datetime.datetime.now)

    class Meta:
        """Описание метакласса Территориальный орган федерального казначейства."""

        verbose_name = 'Территориальный орган федерального казначейства'
        verbose_name_plural = 'Территориальные органы федерального казначейства'

    def __str__(self):
        """Строковое представление Территориальный орган федерального казначейства."""
        pass


# ! КОСГУ/кцср
class KOSGU(models.Model):
    """Описание модели Справочник классификации операций сектора государственного управления. КОСГУ."""

    # TODO: Define fields here
    guid               = models.CharField("Глобально-уникальный идентификатор записи", max_length=36, blank=False, null=False, default='', validators=[MinLengthValidator(36)])
    startdate          = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    enddate            = models.DateTimeField("Дата окончания действия записи")
    status             = models.CharField("Статус записи", max_length=7, choices=KBKStatus.choices, blank=False, null=False)
    code               = models.CharField("Код", max_length=3, blank=False, null=False, unique=True)
    shortname          = models.TextField("Сокращенное наименование", max_length=254)
    fullname           = models.TextField("Полное наименование", max_length=2000, blank=False, null=False)
    parentcode         = models.ForeignKey('self', verbose_name="Код вышестоящего", blank=True, null=True, on_delete=models.SET_NULL)
    tofkcode           = models.ForeignKey(TOFK, verbose_name="Код целевой статьи", blank=False, null=False, on_delete=models.CASCADE)
    dateinclusion      = models.DateTimeField("Дата включения кода", blank=False, null=False, default=datetime.datetime.now)
    dateexclusion      = models.DateTimeField("Дата исключения кода")
    loaddate           = models.DateTimeField("Дата загрузки на ЕПБС", blank=False, null=False, default=datetime.datetime.now)
    filedate           = models.DateTimeField("Дата файла, дата выгрузки из сводного реестра", blank=False, null=False, default=datetime.datetime.now)

    class Meta:
        """Описание метакласса Справочник классификации операций сектора государственного управления."""

        verbose_name = 'Справочник классификации операций сектора государственного управления'
        verbose_name_plural = 'Справочники классификаций операций сектора государственного управления'

    def __str__(self):
        """Строковое представление Справочник классификации операций сектора государственного управления."""
        return f"{self.code}: {self.fullname}"


# ! Справочник типов бюджета
class BudgetType(models.Model):
    """Описание модели Справочник типов бюджета."""
    code               = models.CharField("Код", max_length=2, blank=False, null=False, unique=True)
    name               = models.CharField("Наименование", max_length=127, blank=False, null=False)

    class Meta:
        """Описание метакласса Справочник типов бюджета."""

        verbose_name = 'Справочник типов бюджета'
        verbose_name_plural = 'Справочники типов бюджета'

    def __str__(self):
        """Строковое представление Справочник типов бюджета."""
        return f"{self.code}: {self.name}"


# ! Бюджеты -- убрать ReferenceBook
class Budget(models.Model):
    """Описание модели Справочник бюджетов."""

    # TODO: Define fields here
    # guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36)  # ! Не берем при импорте
    code                = models.CharField("Код", max_length=8, blank=False, null=False)
    name                = models.TextField("Полное наименование", max_length=2000, blank=False, null=False)
    parentcode          = models.ForeignKey('self', verbose_name="Код вышестоящего", blank=True, null=True, on_delete=models.SET_NULL)
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    enddate             = models.DateTimeField("Дата окончания действия записи", blank=True, null=True)
    status              = models.CharField("Статус записи", max_length=7, choices=KBKStatus.choices, blank=False, null=False, default=KBKStatus.ACTIVE)
    budgettype          = models.ForeignKey(BudgetType, verbose_name="Код вышестоящего", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        """Описание метакласса Справочник бюджетов."""

        verbose_name = 'Справочник бюджетов'
        verbose_name_plural = 'Справочники бюджетов'

    def __str__(self):
        """Строковое представление Справочник бюджетов."""
        return f"{self.code}: {self.name}"


# ! Главы по бюджетной классификации - пока грузим в 2 таблицы для упрощения
class GlavBudgetClass(models.Model):
    """Описание модели Справочник главы по бюджетной классификации."""

    # guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36)
    code                = models.CharField("Код", max_length=3, blank=False, null=False)  # ! если не будут пересекаться добавить: , unique=True
    shortname           = models.TextField("Сокращенное наименование", max_length=254)
    fullname            = models.TextField("Полное наименование", max_length=2000, blank=False, null=False)
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    enddate             = models.DateTimeField("Дата окончания действия записи")
    status              = models.CharField("Статус записи", max_length=7, choices=KBKStatus.choices, blank=False, null=False)
    budget              = models.ForeignKey(Budget, verbose_name="Код бюджета", blank=False, null=False, on_delete=models.CASCADE)
    # tofkcode
    # ppocode
    dateinclusion       = models.DateTimeField("Дата включения кода", blank=False, null=False, default=datetime.datetime.now)
    dateexclusion       = models.DateTimeField("Дата исключения кода")
    # year                = models.DateField("Год")

    class Meta:
            """Описание метакласса Справочник главы по бюджетной классификации."""

            verbose_name = 'Справочник главы по бюджетной классификации'
            verbose_name_plural = 'Справочники главы по бюджетной классификации'

    def __str__(self):
        """Строковое представление Главный распорядитель бюджетных средств."""
        return f"{self.code}: {self.fullname}"


# ! В 1с Главные распорядители объединены с Главами по БК в Справочник Главы по бюджетной классификации
# ! ГРБС - Главный Распорядитель Бюджетных Средств
class GlavnRaspBudgetSred(models.Model):
    """Описание модели Главный распорядитель бюджетных средств. ГРБС"""

    # TODO: Define fields here
    code                = models.CharField("Код", max_length=3, blank=False, null=False, unique=True)
    name                = models.TextField("Наименование", max_length=2000, blank=False, null=False)
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    enddate             = models.DateTimeField("Дата окончания действия записи")
    budgcode            = models.ForeignKey(Budget, verbose_name="Код бюджета", blank=False, null=False, on_delete=models.CASCADE)
    # ppocode =          = models.ForeignKey(Ppo, verbose_name="ППО", blank=False, null=False, on_delete=models.CASCADE)  # ! Пока не заполнена ППО - не грузим
    year                = models.DateField("Год")
    # npa                = models.ForeignKey(Npa, verbose_name="НПА", blank=False, null=False, on_delete=models.CASCADE)
    # stagename          = models.TextField("Наименование этапа", max_length=255, blank=False, null=False) # Пример: Формирование закона (решения) о бюджете # ! В 1с справочника нет

    class Meta:
        """Описание метакласса Главный распорядитель бюджетных средств."""

        verbose_name = 'Главный распорядитель бюджетных средств'
        verbose_name_plural = 'Главные распорядители бюджетных средств'

    def __str__(self):
        """Строковое представление Главный распорядитель бюджетных средств."""
        return f"{self.code}: {self.name}"


# ! Главы по БК
class KodVedomstv(models.Model):
    """Описание модели Справочник кодов ведомств."""

    # TODO: Define fields here
    # guid =              models.UUIDField("Глобально-уникальный идентификатор записи", primary_key=True, default=uuid.uuid4, max_length=36)
    guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36, blank=False, null=False, default='', validators=[MinLengthValidator(36)])
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    enddate             = models.DateTimeField("Дата окончания действия записи")
    status              = models.CharField("Статус записи", max_length=7, choices=KBKStatus.choices, blank=False, null=False)  # ! Есть ли смысл хранить отдельно, если информация ясна из дат
    code                = models.CharField("Код", max_length=3, blank=False, null=False, unique=True)
    shortname           = models.TextField("Сокращенное наименование", max_length=254)
    fullname            = models.TextField("Полное наименование", max_length=2000, blank=False, null=False)
    parentcode          = models.ForeignKey('self', verbose_name="Код вышестоящего", blank=True, null=True, on_delete=models.SET_NULL)  # ! Скорее всего справочник не иерархический, скорее всего поле не нужно
    budgcode            = models.ForeignKey(Budget, verbose_name="Код бюджета", blank=False, null=False, on_delete=models.CASCADE)
    tofkcode            = models.ForeignKey(TOFK, verbose_name="Код целевой статьи", blank=False, null=False, on_delete=models.CASCADE)
    dateinclusion       = models.DateTimeField("Дата включения кода", blank=False, null=False, default=datetime.datetime.now)
    dateexclusion       = models.DateTimeField("Дата исключения кода")
    loaddate            = models.DateTimeField("Дата загрузки на ЕПБС", blank=False, null=False, default=datetime.datetime.now)  # ! Поля связаны с обменом - хранить  -- возможно
    filedate            = models.DateTimeField("Дата файла, дата выгрузки из сводного реестра", blank=False, null=False, default=datetime.datetime.now)  # ! Поля связаны с обменом - хранить  -- возможно

    class Meta:
        """Описание метакласса Справочник кодов ведомств."""

        verbose_name = 'Справочник кодов ведомств'
        verbose_name_plural = 'Справочники кодов ведомств'

    def __str__(self):
        """Строковое представление Справочник кодов ведомств."""
        return f"{self.code}: {self.fullname}"

#! В 1с - Код раздела и подраздела КРБ
class KodRazdelIPodrazdel(models.Model):
    """Описание модели Перечень и коды разделов и подразделов БК."""

    # TODO: Define fields here
    code                = models.CharField("Код", max_length=4, blank=False, null=False, unique=True)
    name                = models.TextField("Наименование", max_length=2000, blank=False, null=False)
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    budgcode            = models.ForeignKey(Budget, verbose_name="Код бюджета", blank=False, null=False, on_delete=models.CASCADE)
    # pponame =           models.TextField("Наименование ППО", max_length=2000, blank=False, null=False)
    ppocode             = models.ForeignKey(PPO, verbose_name="ППО", blank=False, null=False, on_delete=models.CASCADE)
    level               = models.CharField("Уровень", max_length=2)  # ! В 1с уровни не хранятся, но есть признак групп(bool)
    year                = models.CharField("Год", max_length=4)
    enddate             = models.DateTimeField("Дата окончания действия записи")
    npa                 = models.ForeignKey(NPA, verbose_name="НПА", blank=False, null=False, on_delete=models.CASCADE)
    stagename           = models.TextField("Наименование этапа", max_length=2000, blank=False, null=False)

    class Meta:
        """Описание метакласса Перечень и коды разделов и подразделов БК."""

        verbose_name = 'Перечень и коды разделов и подразделов БК'
        verbose_name_plural = 'Перечни и коды разделов и подразделов БК'

    def __str__(self):
        """Строковое представление Перечень и коды разделов и подразделов БК."""
        return f"{self.code}: {self.name}"


# ! Целевые статьи
# ! В 1с называется: Целевые статьи КРБ
# ! В 1с есть ссылка на Справочник Бюджеты
class CelevStatKRB(models.Model):
    """
        Описание модели Перечень кодов целевых статей бюджета субъекта РФ, территориального гос внебюджетного фонда, местного бюджета.
    """

    # TODO: Define fields here
    code                = models.CharField("Код", max_length=10, blank=False, null=False, unique=True)
    name                = models.TextField("Наименование", max_length=255, blank=False, null=False)
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    # subprogramcode =    models.CharField("Код подпрограммы", max_length=10, blank=False, null=False, unique=True)
    budgcode            = models.ForeignKey(Budget, verbose_name="Код бюджета", blank=False, null=False, on_delete=models.CASCADE)
    # pponame =           models.TextField("Наименование ППО", max_length=2000, blank=False, null=False)
    # ppocode =           models.CharField("Код ППО", max_length=8, blank=False, null=False)
    ppocode             = models.ForeignKey(PPO, verbose_name="ППО", blank=False, null=False, on_delete=models.CASCADE)
    level               = models.CharField("Уровень", max_length=2)
    year                = models.CharField("Год", max_length=4)
    enddate             = models.DateTimeField("Дата окончания действия записи")
    # npa =               models.ForeignKey(Npa, verbose_name="НПА", blank=False, null=False, on_delete=models.CASCADE)
    # stagename =         models.TextField("Наименование этапа", max_length=2000, blank=False, null=False)
    # dbkkscr_id =        models.CharField("dbk классификации целевых статей расходов", max_length=6)
    parentcode          = models.ForeignKey('self', verbose_name="Код вышестоящего", blank=True, null=True, on_delete=models.SET_NULL)
    # parentcode =        models.CharField("Код вышестоящего", max_length=10)  # ! ссылка на code
    # id_code =           models.CharField("id_code", max_length=11)
    # idparent =          models.CharField("id_code_parent", max_length=11)
    # signsistem =        models.CharField("Знаковая система", max_length=1)
    # levelkcsr =         models.CharField("Уровень классификации целевых статей расходов", max_length=2)

    class Meta:
        """Описание метакласса Перечень кодов целевых статей бюджета."""

        verbose_name = 'Перечень кодов целевых статей бюджета'
        verbose_name_plural = 'Перечени кодов целевых статей бюджета'

    def __str__(self):
        """Строковое представление Перечень кодов целевых статей бюджета."""
        return f"{self.code}: {self.name}"


# ! Виды расходов
class VidRashodov(models.Model):
    """Описание модели Справочник кодов видов расходов."""
    # CodesOfExpencyTypesReferenceBook

    # TODO: Define fields here
    # guid =              models.UUIDField("Глобально-уникальный идентификатор записи", primary_key=True, default=uuid.uuid4, max_length=36)
    guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36, validators=[MinLengthValidator(36)])
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    enddate             = models.DateTimeField("Дата окончания действия записи")
    status              = models.CharField("Статус записи", max_length=7, choices=KBKStatus.choices, blank=False, null=False)
    code                = models.CharField("Код", max_length=3, blank=False, null=False, unique=True)
    shortname           = models.TextField("Сокращенное наименование", max_length=254)
    fullname            = models.TextField("Полное наименование", max_length=2000, blank=False, null=False)
    # parentcode =        models.ForeignKey('self.code', verbose_name="Код вышестоящего", max_length=10, on_delete=models.SET_NULL)
    parentcode          = models.ForeignKey('self', verbose_name="Код вышестоящего", blank=True, null=True, on_delete=models.SET_NULL)
    budgcode            = models.ForeignKey(Budget, verbose_name="Код бюджета", blank=False, null=False, on_delete=models.CASCADE)
    tofkcode            = models.ForeignKey(TOFK, verbose_name="Код целевой статьи", blank=False, null=False, on_delete=models.CASCADE)
    dateinclusion       = models.DateTimeField("Дата включения кода", blank=False, null=False, default=datetime.datetime.now)
    dateexclusion       = models.DateTimeField("Дата исключения кода")
    loaddate            = models.DateTimeField("Дата загрузки на ЕПБС", blank=False, null=False, default=datetime.datetime.now)
    filedate            = models.DateTimeField("Дата файла, дата выгрузки из сводного реестра", blank=False, null=False, default=datetime.datetime.now)
    recordid            = models.TextField("ID записи", max_length=100, blank=False, null=False)
    metaid              = models.CharField("Групповой идентификатор", max_length=36, blank=False, null=False)
    parentname          = models.TextField("Наименование родителя", max_length=2000, blank=False, null=False)
    parentmetaid        = models.CharField("Идентификатор записи родителя", max_length=36, blank=False, null=False)

    class Meta:
        """Описание метакласса Справочник кодов видов расходов."""

        verbose_name = 'Справочник кодов видов расходов'
        verbose_name_plural = 'Справочники кодов видов расходов'

    def __str__(self):
        """Строковое представление Справочник кодов видов расходов."""
        return f"{self.code}: {self.name}"


# ! КБК
class KBK(models.Model):
    """Описание модели Справочник кодов бюджетной классификации по расходам."""

    # TODO: Define fields here
    # guid =              models.UUIDField("Глобально-уникальный идентификатор записи", primary_key=True, default=uuid.uuid4, max_length=36)  # сгенерировать потом guid 36 символов длиной
    guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36, validators=[MinLengthValidator(36)])
    guidparent          = models.ForeignKey('self', verbose_name="Родительский GUID", on_delete=models.CASCADE)
    # guidparent =        models.CharField("Родительский GUID", max_length=36, blank=False, null=False, default='')
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    enddate             = models.DateTimeField("Дата окончания действия записи")
    status              = models.CharField("Статус записи", max_length=7, choices=KBKStatus.choices, blank=False, null=False)
    # glavacode =         models.CharField("Код главы", max_length=3, blank=False, null=False)
    glavacode           = models.ForeignKey(GlavBudgetClass, verbose_name="Код главы", blank=False, null=False, on_delete=models.CASCADE)
    # razdelcode =        models.CharField("Код раздела и подраздела", max_length=4, blank=False, null=False)
    razdelcode          = models.ForeignKey(KodRazdelIPodrazdel, verbose_name="Код раздела и подраздела", blank=False, null=False, on_delete=models.CASCADE)
    # itemcode =          models.CharField("Код целевой статьи", max_length=10, blank=False, null=False)
    itemcode            = models.ForeignKey(CelevStatKRB, verbose_name="Код целевой статьи", blank=False, null=False, on_delete=models.CASCADE)
    # expencetypecode =   models.CharField("Код вида расходов", max_length=3, blank=False, null=False)
    expencetypecode     = models.ForeignKey(VidRashodov, verbose_name="Код вида расходов", blank=False, null=False, on_delete=models.CASCADE)
    # kosgucode =         models.CharField("Код КОСГУ", max_length=3)  # ! Нет таблицы КОСГУ
    kosgucode           = models.ForeignKey(KOSGU, verbose_name="Код КОСГУ", blank=False, null=False, on_delete=models.CASCADE)
    code                = models.CharField("Код", max_length=20, blank=False, null=False)
    shortname           = models.TextField("Сокращенное наименование", max_length=254)
    fullname            = models.TextField("Полное наименование", max_length=2000, blank=False, null=False)
    budgcode            = models.ForeignKey(Budget, verbose_name="Код бюджета", blank=False, null=False, on_delete=models.CASCADE)
    islimit             = models.BooleanField("Признак лимитируемых расходов", blank=False, null=False)
    # tofkcode =          models.CharField("Код ТОФК", max_length=8)  # ! Нет таблицы код ТОФК
    tofkcode            = models.ForeignKey(TOFK, verbose_name="Код целевой статьи", blank=False, null=False, on_delete=models.CASCADE)
    dateinclusion       = models.DateTimeField("Дата включения кода", blank=False, null=False, default=datetime.datetime.now)
    dateexclusion       = models.DateTimeField("Дата исключения кода")
    loaddate            = models.DateTimeField("Дата загрузки на ЕПБС", blank=False, null=False, default=datetime.datetime.now)
    filedate            = models.DateTimeField("Дата файла, дата выгрузки из сводного реестра", blank=False, null=False, default=datetime.datetime.now)

    class Meta:
        """Описание метакласса Справочник кодов бюджетной классификации по расходам."""

        verbose_name = 'Справочник кодов бюджетной классификации по расходам'
        verbose_name_plural = 'Справочники кодов бюджетной классификации по расходам'

    def __str__(self):
        """Строковое представление Справочник кодов бюджетной классификации по расходам."""
        return f"{self.code}: {self.fullname}"

    # def save(self):
    #     # ! Написать проверку длины поля itemcode при сохранении и отсюда уже выставлять дату
    #     pass
