from django.contrib import admin
from models import dyn_models, models_data
# Register your models here.
for name, model in dyn_models.iteritems():
    admin.site.register(model, type(name+'Admin', (admin.ModelAdmin,), {'list_display':[f['id'] for f in models_data[name]['fields']]}))
