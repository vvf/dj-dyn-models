import random
import json
from datetime import date
from django.core.serializers import serialize
from django.test import TestCase
from django.test import Client
from django.db import models

# Create your tests here.
from django.test.utils import override_settings
from django.utils.datetime_safe import datetime
from dynmodels.models import models_data, dyn_models

def _get_random(of_type):
    if of_type == 'int':
        return random.randint(-500, 10000000)
    elif of_type == 'date':
        return date.fromtimestamp(random.randint(600000000, 1400000000))
    elif of_type == 'char':
        return ''.join([chr(random.randint(32, 127)) for i in xrange(random.randint(50, 100))])


def _get_random_as_str(of_type):
    if of_type == 'int':
        return str(random.randint(-500, 10000000))
    elif of_type == 'date':
        return datetime.fromtimestamp(random.randint(600000000, 1400000000)).strftime("%d.%m.%Y")
    elif of_type == 'char':
        return ''.join([chr(random.randint(32, 127)) for i in xrange(random.randint(50, 100))])

types_map = dict(
    char=basestring,
    int=int,
    date=date
)

# @override_settings(LANGUAGE_CODE='ru_ru')
class TestCommon( TestCase ):
    client = Client()

    def setUp(self):
        pass

    def test_models(self):
        for model_name, meta_data in models_data.iteritems():
            assert issubclass(dyn_models[model_name], models.Model)
            obj = dyn_models[model_name].objects.create(**dict(((field['id'], _get_random(field['type'])) for field in meta_data['fields'])))
            obj = dyn_models[model_name].objects.get(id=obj.id)
            for field in meta_data['fields']:
                assert hasattr(obj, field['id'])
                assert isinstance(getattr(obj, field['id']), types_map[field['type']])

    def _test_saving(self, model_name, meta_data, update_id=None):
        post_data = dict(((field['id'], _get_random_as_str(field['type'])) for field in meta_data['fields']))
        if update_id is not None:
            post_data['id'] = update_id
        resp = self.client.post('/api/{}/'.format(model_name), post_data)
        assert resp.status_code == 200
        result = json.loads(resp.content, resp._charset)
        assert result['success']
        if update_id is not None:
            assert int(update_id) == int(result['row_id'])
        obj = dyn_models[model_name].objects.get(id=result['row_id'])
        # compare fields of obj and sended post_data
        for field in meta_data['fields']:
            field_value = getattr(obj, field['id'])
            if field['type'] == 'date':
                assert field_value.strftime('%d.%m.%Y') == post_data[field['id']]
            elif field['type'] == 'int':
                assert field_value == int(post_data[field['id']])
            else:
                assert field_value == post_data[field['id']]
        return obj

    def test_api(self):
        #Create several items of each models
        for model_name, meta_data in models_data.iteritems():
            for i in xrange(random.randint(2, 5)):
                # test create
                obj = self._test_saving(model_name,meta_data, None)
                # test update
                self._test_saving(model_name,meta_data, obj.id)

                # test invalid data
                post_data = dict(((field['id'], _get_random_as_str('char')) for field in meta_data['fields']))

                resp = self.client.post('/api/{}/'.format(model_name), post_data)
                result = json.loads(resp.content, resp._charset)
                assert resp.status_code==200
                assert not result['success']
                assert result['errors']

        # test list
        for model_name, meta_data in models_data.iteritems():
            resp = self.client.get('/api/{}/'.format(model_name), post_data)
            assert resp.status_code==200
            objects = dyn_models[model_name].objects.all()[0:30]
            assert resp.content == serialize('json', objects)
