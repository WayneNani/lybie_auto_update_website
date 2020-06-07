import datetime
import requests

import website_builder.util_credentials as util_credentials

WEBSERVICE_URL = util_credentials.webservice_url()


def get_webservice_url(module):
    url = WEBSERVICE_URL + module
    return url


def get_place_data(last_access=datetime.datetime(1970, 1, 1, )):
    response = requests.get(get_webservice_url('places/places'),
                            headers={'last_access': last_access.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'})

    return response.json()['items']


def get_images_for_place(place_id):
    response = requests.get(get_webservice_url('images/place_images'),
                            headers={'id_place': f'{place_id}'})

    return response.json()['items']


def get_template(template_type):
    response = requests.get(get_webservice_url('templates/template'),
                            headers={'template_type': f'{template_type}'})

    return response.json()['template_content']


def get_image(id_image):
    response = requests.get(get_webservice_url('images/image'),
                            headers={'id_image': f'{id_image}'})

    return response.content


def get_static_varchar(name):
    response = requests.get(get_webservice_url('parameters/varchar_parameter'),
                            headers={'parameter_name': f'{name}'})

    return response.json()['value']


def get_static_date(name):
    response = requests.get(get_webservice_url('parameters/date_parameter'),
                            headers={'parameter_name': f'{name}'})

    return response.json()['value']


def get_static_number(name):
    response = requests.get(get_webservice_url('parameters/number_parameter'),
                            headers={'parameter_name': f'{name}'})

    return response.json()['value']


def update_last_access(varchar_value=None, date_value=None, number_value=None):
    response = requests.put(get_webservice_url('parameters/parameter'),
                            headers={'varchar_value': f'{varchar_value}',
                                     'date_value': date_value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                                     'number_value': number_value,
                                     'parameter_name': 'LAST_ACCESS'})

    if response.status_code != 200:
        raise Exception('Error while Updating last_access')
