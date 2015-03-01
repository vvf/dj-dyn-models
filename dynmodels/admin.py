from django.contrib import admin
from models import dyn_models
# Register your models here.
for name, model in dyn_models.iteritems():
    admin.site.register(model, type(name+'Admin',(admin.ModelAdmin,),{}) )
