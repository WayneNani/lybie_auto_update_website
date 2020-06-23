import datetime
import requests


class Webservice:

    def __init__(self, base_url):
        self.BASE_URL = base_url

    def http_get(self, module, headers):
        response = requests.get(url=self.BASE_URL + module,
                                headers=headers)

        return response

    def get_webservice_url(self, module):
        url = self.BASE_URL + module
        return url

    def get_place_data(self, last_access=datetime.datetime(1970, 1, 1, )):
        response = requests.get(self.get_webservice_url('places/places'),
                                headers={'last_access': last_access.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'})

        return response.json()['items']

    def get_images_for_place(self, place_id):
        response = requests.get(self.get_webservice_url('images/place_images'),
                                headers={'id_place': f'{place_id}'})

        return response.json()['items']

    def get_template(self, template_type):
        response = requests.get(self.get_webservice_url('templates/template'),
                                headers={'template_type': f'{template_type}'})

        return response.json()['template_content']

    def get_image(self, id_image):
        response = requests.get(self.get_webservice_url('images/image'),
                                headers={'id_image': f'{id_image}'})

        return response.content

    def get_static_varchar(self, name):
        response = requests.get(self.get_webservice_url('parameters/varchar_parameter'),
                                headers={'parameter_name': f'{name}'})

        return response.json()['value']

    def get_static_date(self, name):
        response = requests.get(self.get_webservice_url('parameters/date_parameter'),
                                headers={'parameter_name': f'{name}'})

        return response.json()['value']

    def get_static_number(self, name):
        response = requests.get(self.get_webservice_url('parameters/number_parameter'),
                                headers={'parameter_name': f'{name}'})

        return response.json()['value']

    def update_last_access(self, date_value=None):
        response = requests.put(self.get_webservice_url('parameters/parameter'),
                                headers={'date_value': date_value.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                         'parameter_name': 'LAST_ACCESS'})

        if response.status_code != 200:
            raise Exception('Error while Updating last_access')
