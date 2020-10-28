from django.contrib import admin
from . import models
import inspect


# Register your models here.
for model_name in dir(models):
    model = getattr(models, model_name)
    # print(model)
    if isinstance(model, models.models.base.ModelBase):
        admin.site.register(model)

# admin.register(models.Npa)
# admin.register(models.Ppo)
# admin.register(models.TerritorialDepartmentFederalTreasuryReferenceBook)
# admin.register(models.ClassificationOfGeneralGovernmentTransactions)
# admin.register(models.BudgetTypeReferenceBook)
# admin.register(models.BudgetReferenceBook)
# admin.register(models.HeadsOfBudgetClassificationReferenceBook)
# admin.register(models.SectionAndSubsectionListAndCodesBudgetClassification)
# admin.register(models.ListOfCodesOfTargetBudgetExpenditures)
# admin.register(models.ReferenceOfCodesOfCostTypes)
# admin.register(models.CostsBudgetClassificationCodesReferenceBook)
