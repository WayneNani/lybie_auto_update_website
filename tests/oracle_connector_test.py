import json
import os
import datetime

import website_builder.oracle_connector as ora


def test_oracle_place_data():
    DATA_FOLDER = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(DATA_FOLDER, 'credentials.json')
    CREDENTIALS = json.load(open(DATA_PATH), encoding='utf-8')
    db_connection_string = f'{CREDENTIALS.get("ORACLE_DB_USER_TEST")}/{CREDENTIALS.get("ORACLE_DB_PASSWORD_TEST")}' \
                        f'@{CREDENTIALS.get("ORACLE_DB_IP")}:1539/xepdb1'

    with ora.connect(db_connection_string) as con:
        place = ora.get_place_data(con)[0]

        assert place['id'] == 1
        assert place['place_name'] == 'place01'
        assert place['text_de'] == 'testText_DE'
        assert place['text_en'] == 'testText_EN'
        assert place['location_de'] == 'locDE'
        assert place['location_en'] == 'locEN'
        assert place['file_name'] == 'herz-blüten.jpg'
        assert place['id_thumbnail'] == 22
        assert place['creation_date'] == datetime.datetime(2018, 5, 6,)
        assert place['date_modified'] == datetime.datetime(2020, 4, 10,)


def test_oracle_image():
    DATA_FOLDER = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(DATA_FOLDER, 'credentials.json')
    CREDENTIALS = json.load(open(DATA_PATH), encoding='utf-8')
    db_connection_string = f'{CREDENTIALS.get("ORACLE_DB_USER_TEST")}/{CREDENTIALS.get("ORACLE_DB_PASSWORD_TEST")}' \
                        f'@{CREDENTIALS.get("ORACLE_DB_IP")}:1539/xepdb1'

    with ora.connect(db_connection_string) as con:
        image = ora.get_images_for_place(con, 1)[0]

        assert image['id'] == 22
