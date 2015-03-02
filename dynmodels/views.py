from django import forms
from django.contrib.admin import widgets
from django.core.serializers import serialize
from django.forms.models import ModelForm
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_POST
from dynmodels.models import *

# Create your views here.
from dynmodels.models import models_data
import json

def main(request):
    tpl_vars = dict(
        models_data_json=json.dumps(models_data),
        models_data=models_data,
    )
    return render(request,'main.html', tpl_vars)


def list(request, table):
    if request.method == 'POST':
        return save(request, table)
    if table not in dyn_models:
        return HttpResponseNotFound()
    page = request.GET.get('page', 0)
    limit = request.GET.get('limit', 30)
    result = dyn_models[table].objects.all()[page:(page+1)*limit]
    return HttpResponse(serialize('json', result))

forms = dict([(tbl,
               type(tbl,
                    (ModelForm,),
                    {'__module__': __name__,
                     'Meta': type('Meta', (), dict(model=model, fields=[f['id'] for f in models_data[tbl]['fields']]))
                    })
              ) for tbl, model in dyn_models.iteritems()])

def save(request, table, row_id=None):
    if table not in dyn_models:
        return HttpResponseNotFound()
    obj = None
    if row_id is None and request.POST.get('id', '').isdigit():
        row_id = request.POST['id']
    if row_id is not None:
        obj = dyn_models[table].objects.filter(id=row_id).first()
    form = forms[table](request.POST, instance=obj)
    if form.is_valid():
        obj = form.save()
        return HttpResponse(json.dumps(dict(success=True, row_id=obj.id)))

    return HttpResponse(json.dumps(dict(success=False, errors=form.errors)))
