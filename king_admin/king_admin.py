#__author:  Administrator
#date:  2017/1/5

from crm import models


enabled_admins = {}


class BaseAdmin(object):
    list_display = []
    list_filters = []
    list_per_page = 20
    search_fields = []
    ordering = None
    filter_horizontal = []

class CustomerAdmin(BaseAdmin):
    list_display = ['id','qq','name','source','consultant','consult_course','date','status']
    list_filters = ['source','consultant','consult_course','status','date']
    search_fields = ["qq","name","consultant__name"]
    list_per_page = 5
    ordering = "id"
    filter_horizontal = ('tags',)
    #model = models.Customer


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer','consultant','date')


def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {} #enabled_admins['crm'] = {}
    #admin_obj = admin_class()
    admin_class.model = model_class #绑定model 对象和admin 类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class
    #enabled_admins['crm']['customerfollowup'] = CustomerFollowUpAdmin
    # CustomerFollowUpAdmin.model = crm.CustomerFollowUp
    #enabled_admins['crm']['customer'] = CustomerAdmin
    # CustomerAdmin.model = crm.Customer


register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)



