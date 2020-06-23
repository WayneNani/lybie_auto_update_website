import datetime
import os

import website_builder.oracle_connector as oc
import website_builder.util_credentials as util_credentials

WEBSERVICE_BASE_URL = util_credentials.webservice_url(
    util_credentials.load_config(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')))


def test_oracle_place_data():
    data = {
        'id': 1,
        'place_name': 'place01',
        'text_de': 'testText_DE',
        'text_en': 'testText_EN',
        'location_de': 'locDE',
        'location_en': 'locEN',
        'file_name': 'herz-blüten.jpg',
        'id_thumbnail': 22,
        'creation_date': datetime.datetime(2018, 5, 5, 22, ).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'date_modified': datetime.datetime(2020, 4, 9, 22, ).strftime('%Y-%m-%dT%H:%M:%SZ'),
    }
    connector = oc.Webservice(WEBSERVICE_BASE_URL)

    place = connector.get_place_data()[0]
    assert place == data


def test_oracle_image_mapping():
    data = {
        'id': 22,
        'file_name': 'herz-blüten.jpg'
    }
    connector = oc.Webservice(WEBSERVICE_BASE_URL)

    image = connector.get_images_for_place(1)[0]
    assert image == data


def test_oracle_multiple_images_mapping():
    data = [{'id': 61, 'file_name': 'place3_stones.jpg'},
            {'id': 101, 'file_name': 'place3_baum.jpg'},
            {'id': 102, 'file_name': 'place3_kristall.jpg'}]
    connector = oc.Webservice(WEBSERVICE_BASE_URL)

    image = connector.get_images_for_place(41)
    assert image == data


def test_oracle_no_image_mapping():
    data = []
    connector = oc.Webservice(WEBSERVICE_BASE_URL)

    image = connector.get_images_for_place(-3)
    assert image == data


def test_oracle_template():
    data = "+++\nshowonlyimage = false\ndraft = false\nimage = \"[THUMBNAIL]\"\ndate = \"[" \
           "DATE]T18:25:22+05:30\"\nweight = 102\ndescription = \"[LOCATION]\"\n+++\n\n[IMAGE]\n\n[TEXT]"
    connector = oc.Webservice(WEBSERVICE_BASE_URL)

    template = connector.get_template('PLACE')

    assert template == data


def test_oracle_static_varchar():
    data = 'DE'
    connector = oc.Webservice(WEBSERVICE_BASE_URL)

    aufenthaltsort = connector.get_static_varchar('AUFENTHALTSORT')

    assert aufenthaltsort == data


def test_oracle_static_date():
    data = '2020-04-13T00:00:00Z'
    connector = oc.Webservice(WEBSERVICE_BASE_URL)

    last_access = connector.get_static_date('DUMMY_DATE')

    assert last_access == data


def test_oracle_retrieve_image():
    image_park = open(os.path.join('tests', 'redoutenpark.jpg'), 'rb').read()
    connector = oc.Webservice(WEBSERVICE_BASE_URL)

    assert connector.get_image(1) == image_park


def test_oracle_update_last_access():
    connector = oc.Webservice(WEBSERVICE_BASE_URL)

    connector.update_last_access(date_value=datetime.datetime.now())
    assert True
