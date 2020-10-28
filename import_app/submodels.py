--В классификаторы
--Над Npa
class Okved(models.Model):
    """Описание модели Общероссийский классификатор видов экономической деятельности ."""

    # TODO: Define fields here
    code = models.CharField("Код ОКВЭД", max_length=8, blank=False, null=False)
    name = models.TextField("Наименование ОКВЭД", max_length=2000, blank=False, null=False)

    class Meta:
        """Описание метакласса Общероссийский классификатор видов экономической деятельности"""
        verbose_name = "Общероссийский классификатор видов экономической деятельности"
        verbose_name_plural = "Общероссийские классификаторы видов экономической деятельности"

    def __str__(self):
        """Строковое представление Общероссийский классификатор видов экономической деятельности."""
        return f"{self.code}: {self.name}"


class Okpd(models.Model):
    """Описание модели Общероссийский классификатор продукции."""

    # TODO: Define fields here
    code = models.CharField("Код ОКПД", max_length=12, blank=False, null=False)
    name = models.TextField("Наименование ОКПД", max_length=2000, blank=False, null=False)

    class Meta:
        """Описание метакласса Общероссийский классификатор продукции"""
        verbose_name = "Общероссийский классификатор продукции"
        verbose_name_plural = "Общероссийские классификаторы продукции"

    def __str__(self):
        """Строковое представление Общероссийский классификатор продукции."""
        return f"{self.code}: {self.name}"


class Pay(models.Model):
    """Описание модели Признак платности или бесплатности."""

    # TODO: Define fields here
    code = models.CharField("Код признака платности или бесплатности", max_length=8, blank=False, null=False)
    name = models.TextField("Наименование признака платности или бесплатности", max_length=127, blank=False, null=False)

    class Meta:
        """Описание метакласса Признак платности или бесплатности."""

        verbose_name = 'Признак платности или бесплатности'
        verbose_name_plural = 'Признаки платности или бесплатности'

    def __str__(self):
        """Строковое представление Признак платности или бесплатности."""
        return f"{self.code}: {self.name}"



--Под Npa
--Над Ppo
class Content(models.Model):
    """Описание модели Контент."""

    pblcharcode =       models.CharField("Публичный код характеристики", max_length=11)
    charcode =          models.CharField("Внутренний код характеристики", max_length=3, blank=False, null=False)
    charname =          models.TextField("Наименование характеристики", max_length=2000, blank=False, null=False)
    indexpblcharcode =  models.CharField("Публичный код показателя характеристики", max_length=7)
    namenpa =           models.TextField("НПА", max_length=2000)
    indexcharcode =     models.CharField("Публичный код показателя характеристики", max_length=3, blank=False, null=False)
    indexcharname =     models.TextField("Наименование показателя характеристики", max_length=2000, blank=False, null=False)

    class Meta:
        """Описание метакласса Контент."""
        verbose_name = "Контент"
        verbose_name_plural = "Контенты"

    def __str__(self):
        """Строковое представление Контент."""
        return f"{self.charcode}: {self.charname}"


class Term(models.Model):
    """Описание модели Термин."""

    # TODO: Define fields here
    pblcharcode =       models.CharField("Публичный код характеристики", max_length=11)
    charcode =          models.CharField("Внутренний код характеристики", max_length=3, blank=False, null=False)
    charname =          models.TextField("Наименование характеристики", max_length=2000, blank=False, null=False)
    indexpblcharcode =  models.CharField("Публичный код показателя характеристики", max_length=7)
    namenpa =           models.TextField("НПА", max_length=2000)
    indexcharcode =     models.CharField("Публичный код показателя характеристики", max_length=2, blank=False, null=False)
    indexcharname =     models.TextField("Наименование показателя характеристики", max_length=2000, blank=False, null=False)

    class Meta:
        """Описание метакласса Термин."""
        verbose_name = "Термин"
        verbose_name_plural = "Термины"

    def __str__(self):
        """Строковое представление Термин."""
        return f"{self.charcode}: {self.charname}"
--Под Ppo
class Institute(models.Model):
    """Описание модели Вид учреждения."""

    # TODO: Define fields here
    code =      models.CharField("Код вида учреждения", max_length=7, blank=False, null=False)
    name =      models.TextField("Наименование вида учреждения", max_length=2000, blank=False, null=False)
    namenpa =   models.TextField("НПА", max_length=2000)

    class Meta:
        """Описание метакласса Вид учреждения."""

        verbose_name = 'Вид учреждения'
        verbose_name_plural = 'Виды учреждений'

    def __str__(self):
        """Строковое представление Вид учреждения."""
        return f"{self.code}: {self.name}"


class Consumer(models.Model):
    """Описание модели Категория потребителей."""

    # TODO: Define fields here
    code =      models.CharField("Код категории потребителей", max_length=7, blank=False, null=False)
    name =      models.TextField("Наименование категории потребителей", max_length=2000, blank=False, null=False)
    namenpa =   models.TextField("НПА", max_length=2000)

    class Meta:
        """Описание метакласса Категория потребителей."""

        verbose_name = 'Категория потребителей'
        verbose_name_plural = 'Категории потребителей'

    def __str__(self):
        """Строковое представление Категория потребителей."""
        return f"{self.code}: {self.name}"


class Quality(models.Model):
    """Описание модели Показатель качества."""

    # TODO: Define fields here
    code =      models.CharField("Код показателя качества", max_length=3, blank=False, null=False)
    name =      models.TextField("Наименование показателя качества", max_length=2000, blank=False, null=False)
    unit =      models.TextField("Единицы измерения по ОКЕИ", max_length=127, blank=False, null=False)
    okeicode =  models.CharField("Код единицы измерения по ОКЕИ", max_length=4)

    class Meta:
        """Описание метакласса Показатель качества."""

        verbose_name = 'Показатель качества'
        verbose_name_plural = 'Показатели качества'

    def __str__(self):
        """Строковое представление Показатель качества."""
        return f"{self.code}: {self.name}"


class Volume(models.Model):
    """Описание модели Показатель объема."""

    # TODO: Define fields here
    code =      models.CharField("Код показателя объема", max_length=3, blank=False, null=False)
    name =      models.TextField("Наименование показателя объема", max_length=2000, blank=False, null=False)
    unit =      models.TextField("Единицы измерения по ОКЕИ", max_length=127, blank=False, null=False)
    okeicode =  models.CharField("Код единицы измерения по ОКЕИ", max_length=4)

    class Meta:
        """Описание метакласса Показатель объема."""

        verbose_name = 'Показатель объема'
        verbose_name_plural = 'Показатела объема'

    def __str__(self):
        """Строковое представление Показатель объема."""
        return f"{self.code}: {self.name}"


class InstituteType(models.Model):
    """Описание модели Тип учреждения."""

    # TODO: Define fields here
    code =          models.CharField("Код типа учреждения", max_length=7, blank=False, null=False)
    shortname =     models.CharField("Сокращенное наименование типа учреждения", max_length=7, blank=False, null=False)
    fullname =      models.TextField("Полное наименование типа учреждения", max_length=4000, blank=False, null=False)

    class Meta:
        """Описание метакласса Тип учреждения."""

        verbose_name = 'Тип учреждения'
        verbose_name_plural = 'Типы учреждений'

    def __str__(self):
        """Строковое представление Тип учреждения."""
        return f"{self.code}: {self.shortname}"


class Docinform(models.Model):
    """Описание модели Документ."""

    # TODO: Define fields here
    numberdoc =         models.CharField("Номер документа", max_length=50, blank=False, null=False)
    listnumbermain =    models.CharField("Номер основного документа", max_length=50, blank=False, null=False)
    dockind =           models.CharField("Номер основного документа", max_length=50, blank=False, null=False)
    approverdate =      models.DateTimeField("Дата утверждения документа", blank=False, null=False)
    effectivebefore =   models.DateTimeField("Дата окончания действия документа", blank=False, null=False)
    approvfio_list =    models.TextField("ФИО утверждающего перечень", max_length=2000)
    approvposition =    models.TextField("Должность утверждающего перечень", max_length=2000)
    approvalform =      models.TextField("Форма утверждения", max_length=2000)

    class Meta:
        """Описание метакласса Документ."""

        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        """Строковое представление Документ."""
        pass


class SignOfReferenceToWordOrService(models.IntegerChoices):
    """Признак отнесения к работе/услуге"""
    SERVICE = 0, description('Услуга')
    WORK = 1, description('Работа')


class Classificator(models.Model):
    """Описание модели Классификатор."""

    # TODO: Define fields here
    regnumber =             models.CharField("Реестровый номер услуги(старый)", max_length=23, blank=False, null=False)
    regnumbernew =          models.CharField("Реестровый номер услуги(новый)", max_length=24, blank=False, null=False)
    srvcode =               models.CharField("Код услуги(работы)", max_length=24, blank=False, null=False)
    servicename =           models.TextField("Наименование услуги или работы", max_length=2000, blank=False, null=False)
    # signizer =              models.ForeignKey(, verbose_name="Код из справочника Виды классификаторов работ и услуг", blank=False, null=False)  # ! Вместо 2 полей будет 1 со вторичным и ссылкой на справочник
    # sectname =              models.ForeignKey(, verbose_name="Наименование из справочника Виды классификаторов работ и услуг" blank=False, null=False)  # ! по id
    dockind =               models.TextField("Вид документа, содержащий РЗ", max_length=250)
    numberdoc =             models.TextField("Номер документа, содержащий РЗ", max_length=127, blank=False, null=False)
    svckindcode =           models.CharField("Код признака отнесения к услуге или работе", choices=SignOfReferenceToWordOrService.choices, max_length=1, blank=False, null=False)  # enum
    svckindname =           models.TextField("Наименование признака отнесения к услуге или работе", max_length=2000, blank=False, null=False)
    belong210fl =           models.BooleanField("Принадлежит 210 ФЗ", blank=False, null=False)
    belong210flncsrly =     models.BooleanField("Обязательно принадлежит 210 ФЗ", blank=False, null=False)
    approvaldate =          models.DateTimeField("Дата утверждения реестровой записи")
    startdate =             models.DateTimeField("Дата начала действия реестровой записи", blank=False, null=False)
    enddate =               models.DateTimeField("Дата окончания действия реестровой записи", blank=True)
    loaddate =              models.DateTimeField("Дата загрузки файла", blank=False, null=False)
    createdate =            models.DateTimeField("Дата создания реестровой записи", blank=False, null=False)
    filedate =              models.DateTimeField("Дата формирования файла, содержащего информацию о реестровой записи", blank=False, null=False)
    actual =                models.BooleanField("Признак атуальности услуги(работы)", blank=False, null=False)
    basiclistnumber =       models.CharField("Номер документа ФБПГУ", max_length=23, blank=True)
    actvtycode =            models.CharField("Код вида деятельности", max_length=2, blank=False, null=False)
    actvtyname =            models.TextField("Наименование вида деятельности", max_length=2000, blank=False, null=False)
    foiv =                  models.TextField("Краткое наименование ФОИВ, сформировавшего базовый перечень", max_length=2000, blank=False, null=False)
    foivinn =               models.CharField("ИНН федерального органа исполнительной власти", max_length=10, blank=False, null=False)
    foivcodereestr =        models.CharField("Код по сводному реестру для ФОИВ", max_length=8, blank=False, null=False)
    srvscodenew =           models.CharField("Код наименования услуги, сформированный по новому алгоритму", max_length=4, blank=False, null=False)

    class Meta:
        """Описание метакласса Классификатор."""
        verbose_name = 'Классификатор'
        verbose_name_plural = 'Классификаторы'

    def __str__(self):
        """Строковое представление Классификатор."""
        return f"{self.servicename}"
