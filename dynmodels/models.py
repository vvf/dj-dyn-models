from django.db import models
from django.conf import settings
import yaml
import os

# Create your models here.
# models_yaml = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'models.yaml'), 'r')
models_yaml = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models.yaml'), 'r')

models_data = yaml.load(models_yaml)
dyn_models = {}
attrs = {
    '__module__': __name__,
}
field_types = dict(
    char={'class': models.CharField, 'params': {'max_length': '255', 'blank': 'True', 'null': 'True'}},
    int={'class': models.IntegerField, 'params': {'null': 'True', 'blank': 'True'}},
    date={'class': models.DateField, 'params': {'null': 'True', 'blank': 'True'}}
)
for tbl, params in models_data.iteritems():
    class Meta:
        verbose_name = params['title']

    attrs['Meta'] = Meta
    model = type(tbl, (models.Model,),
                 {'__module__': __name__, 'Meta': type('Meta', (), dict(verbose_name=params['title'],
                                                                        verbose_name_plural=params[
                                                                            'title']))})
    for field_data in params['fields']:
        ftype_meta = field_types[field_data['type']]
        type_params = ftype_meta['params']
        # print ( ftype_meta['class'], type_params )
        #print ftype_meta['class'](**type_params)
        type_params['verbose_name'] = field_data['title']
        model.add_to_class(field_data['id'], ftype_meta['class'](**type_params))
    dyn_models[tbl] = model