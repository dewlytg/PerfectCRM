from django.forms import forms,ModelForm
from django.db import models
from crm import models


class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


def create_model_form(request,admin_class):

    def __new__(cls,*args,**kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs["class"] = "form-control"
        return ModelForm.__new__(cls)

    class Meta:
        model = admin_class.model
        fields = "__all__"

    attrs = {"Meta":Meta}
    # attrs = {"Meta":Meta,"__new__":__new__}
    _model_form_class = type("DynamicClass",(ModelForm,),attrs)
    return _model_form_class
