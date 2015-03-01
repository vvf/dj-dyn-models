from django import forms
from django.contrib.admin import widgets
from django.shortcuts import render

# Create your views here.
from dynmodels.models import models_data
import json


class Form(forms.Form):
    date_fld = forms.DateField(widget=widgets.AdminDateWidget())

def main(request):
    tpl_vars = dict(
        models_data_json=json.dumps(models_data),
        models_data=models_data,
        form=Form()
    )
    return render(request,'main.html', tpl_vars)