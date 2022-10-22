import pytest
import json
from rest_framework import status
from rest_framework.test import APIClient
from bloodtests.models import Test


@pytest.fixture()
def request_client():
    client = APIClient()
    return client


@pytest.mark.django_db()
class TestBloodTests():
    apipath = '/api/bloodtests/test/'

    def test_method_get(self, request_client):
        response = request_client.get(self.apipath + 'ABC')
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_method_head(self, request_client):
        response = request_client.head(self.apipath + 'ABC')
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_method_put(self, request_client):
        response = request_client.put(self.apipath + 'ABC')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_method_post(self, request_client):
        response = request_client.post(self.apipath + 'ABC')
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_method_delete(self, request_client):
        response = request_client.delete(self.apipath + 'ABC')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_method_trace(self, request_client):
        response = request_client.trace(self.apipath + 'ABC')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_method_patch(self, request_client):
        response = request_client.patch(self.apipath + 'ABC')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_method_options(self, request_client):
        response = request_client.options(self.apipath + 'ABC')
        assert response.status_code == status.HTTP_200_OK
        allowed_methods = response['Allow'].replace(' ', '').split(',')
        assert len(allowed_methods) == 4
        assert 'GET' in allowed_methods
        assert 'HEAD' in allowed_methods
        assert 'OPTIONS' in allowed_methods
        assert 'POST' in allowed_methods

    @pytest.mark.parametrize('test, url_code, ideal_range, expected_result', [({'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': 99, 'lower': 45}, 'CHO', {'ideal_range': '45.0 <= value <= 99.0'}, status.HTTP_200_OK),
                                                                              (None, 'CHO', None, status.HTTP_404_NOT_FOUND),
                                                                              ({'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'lower': 45, 'upper': None}, 'CHO', {'ideal_range': 'value >= 45.0'}, status.HTTP_200_OK),
                                                                              ({'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': 99, 'lower': None}, 'CHO', {'ideal_range': 'value <= 99.0'}, status.HTTP_200_OK),
    ])
    def test_get_basic(self, request_client, test, url_code, ideal_range, expected_result):
        # Create a test
        if test:
            Test(**test).save()
            test.update(ideal_range)

        # Run the API
        response = request_client.get(self.apipath + url_code)

        assert response.status_code == expected_result
        content = json.loads(response.content)
        if response.status_code == status.HTTP_200_OK:
            assert content == test

    def test_get_known_errors(self, request_client):
        # Request code that doesn't exist
        response = request_client.get(self.apipath + 'FRED')
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Create a test, and try to access with a different code
        Test(**{'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': 99, 'lower': 45}).save()
        response = request_client.get(self.apipath + 'FRED')
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Alpha numeric code
        Test(**{'code': 'CHO1', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': 99, 'lower': 45}).save()
        response = request_client.get(self.apipath + 'CHO1')
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize('test, url_code, existing, expected_result', [({'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': 99, 'lower': 45}, 'CHO', {}, status.HTTP_200_OK),
                                                                           ({'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': 99, 'lower': 45}, 'CHO',
                                                                            {'code': 'CHO', 'name': 'Cholesterol1', 'unit': 'g/L', 'upper': 98, 'lower': 55}, status.HTTP_200_OK),
                                                                           ({'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': None, 'lower': 45}, 'CHO', {}, status.HTTP_200_OK),
                                                                           ({'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': 33, 'lower': None}, 'CHO', {}, status.HTTP_200_OK),
    ])
    def test_post_basic(self, request_client, test, url_code, existing, expected_result):
        # Create a test
        if test and existing:
            t = Test(**existing)
            t.save()
            assert t.code == existing['code']
            assert t.name == existing['name']
            assert t.unit == existing['unit']
            assert t.upper == existing['upper']
            assert t.lower == existing['lower']


        # Run the API
        print (test)
        response = request_client.post(self.apipath + url_code, content_type='application/json', data=json.dumps(test))

        assert response.status_code == expected_result
        assert len(Test.objects.all()) == 1
        t = Test.objects.first()
        assert t.code == test['code']
        assert t.name == test['name']
        assert t.unit == test['unit']
        assert t.upper == test['upper']
        assert t.lower == test['lower']

    @pytest.mark.parametrize('field', [('name'),
                                       ('unit')
                                       ])
    def test_post_error_missing_fields(self, request_client, field):
        data = {'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/L', 'upper': 99, 'lower': 45}
        data.pop(field)
        response = request_client.post(self.apipath + 'CHO', content_type='application/json', data=json.dumps(data))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        content = json.loads(response.content)
        assert field in content
        assert 'This field is required' in content[field][0]

    @pytest.mark.parametrize('field, value', [('code', 'ABCdE'),
                                              ('name', 'a'*101),
                                              ('unit', 'a'*11)
    ])
    def test_post_error_length_of_fields(self, request_client, field, value):
        data = {'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/L', 'upper': 99, 'lower': 45}
        data[field] = value
        if field == 'code':
            response = request_client.post(self.apipath + value, content_type='application/json', data=json.dumps(data))
        else:
            response = request_client.post(self.apipath + 'CHO', content_type='application/json', data=json.dumps(data))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        content = json.loads(response.content)
        assert field in content
        assert 'Ensure this field has no more than' in content[field][0]

    def test_post_error_lower_null_upper_null(self, request_client):
        data = {'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': 99, 'lower': 45}
        data = {'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M'}
        response = request_client.post(self.apipath + 'CHO', content_type='application/json', data=json.dumps(data))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        content = json.loads(response.content)
        assert 'Lower and upper cannot both be null' in content

    def test_post_error_lower_gt_upper(self, request_client):
        data = {'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': 99, 'lower': 45}
        data = {'code': 'CHO', 'name': 'Cholesterol', 'unit': 'g/M', 'upper': 44, 'lower': 45}
        response = request_client.post(self.apipath + 'CHO', content_type='application/json', data=json.dumps(data))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        content = json.loads(response.content)
        assert "Lower value can't exceed upper value" in content
