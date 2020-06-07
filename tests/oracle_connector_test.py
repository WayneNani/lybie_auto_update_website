import datetime
import os

import website_builder.oracle_connector as oc
import website_builder.util_credentials as util_credentials

DB_CONNECTION_STRING = util_credentials.db_connection_string(
    util_credentials.load_config(
        os.path.join('tests', 'credentials.json')))


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
    place = oc.get_place_data()[0]
    assert place == data


def test_oracle_image_mapping():
    data = {
        'id': 22,
    }
    image = oc.get_images_for_place(1)[0]
    assert image == data


def test_oracle_multiple_images_mapping():
    data = [{'id': 61}, {'id': 101}, {'id': 102}]
    image = oc.get_images_for_place(41)
    assert image == data


def test_oracle_no_image_mapping():
    data = []
    image = oc.get_images_for_place(-3)
    assert image == data
