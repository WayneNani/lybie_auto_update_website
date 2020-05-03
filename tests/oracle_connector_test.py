import datetime

import website_builder.oracle_connector as oc
import website_builder.util as util

DB_CONNECTION_STRING = util.db_connection_string()


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
        'creation_date': datetime.datetime(2018, 5, 6, ),
        'date_modified': datetime.datetime(2020, 4, 10, ),
    }
    with oc.connect(DB_CONNECTION_STRING) as con:
        place = oc.get_place_data(con)[0]
        for key in data.keys():
            assert place[key] == data[key]


def test_oracle_image():
    data = {
        'id': 22,
    }
    with oc.connect(DB_CONNECTION_STRING) as con:
        image = oc.get_images_for_place(con, 1)[0]
        for key in data.keys():
            assert image[key] == data[key]
