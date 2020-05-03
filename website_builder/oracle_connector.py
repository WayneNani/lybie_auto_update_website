import cx_Oracle
import datetime

ENCODING = "UTF-8"

SELECT = {
    "PLACE": (
        """
        SELECT      p.ID, name, text_de, text_en, location_de,
                    location_en, creation_date, file_name, date_modified, i.ID
          FROM      places p
          LEFT JOIN images i ON p.THUMBNAIL = i.ID
          WHERE     date_modified > :last_access
          ORDER BY  p.id ASC
        """),
    "IMAGE_FOR_PLACE": (
        """
        SELECT  ID_IMAGE
          FROM  PLACE_IMAGE_MAPPING
          WHERE ID_PLACE = :id
        """),
    "TEMPLATE": (
        """
        SELECT  template_content
          FROM  templates
          WHERE name = :type
        """),
    "IMAGE": (
        """
        SELECT  file_name, blob_content
          FROM  images
          WHERE id = :id
        """),
    "STATIC_DATA": (
        """
        SELECT  varchar_value, date_value, number_value
          FROM  static_content
          WHERE name = :name
        """),
}

UPDATE = {
    "LAST_ACCESS": (
        """
        UPDATE  static_content
          SET   date_value = :date_value
          WHERE name = 'LAST_ACCESS'
        """
    )
}


def output_type_handler(cursor, name, defaultType, size, precision, scale):
    # Assumption defaultType is in (cx_Oracle.BLOB, cx_Oracle.CLOB)
    magic = cx_Oracle.LONG_BINARY if defaultType == cx_Oracle.BLOB else cx_Oracle.LONG_STRING
    return cursor.var(magic, arraysize=cursor.arraysize)


def connect(db_connect_string):
    return cx_Oracle.connect(db_connect_string, encoding=ENCODING)


def get_place_data(connection, last_access=datetime.datetime(1970, 1, 1, )):
    """Generator of dicts per place entry."""
    labels = (  # matching first db rows entries
        "id", "place_name", "text_de", "text_en", "location_de", "location_en", "creation_date", "file_name",
        "date_modified", "id_thumbnail"
    )
    count = len(labels)
    with connection.cursor() as temp_cursor:
        temp_cursor.execute(SELECT["PLACE"], last_access=last_access)

        for row in temp_cursor.fetchall():
            yield {k: v for k, v in zip(labels, row[:count])}


def get_images_for_place(connection, place_id):
    """Generator of dicts per image for place entry."""
    labels = (  # matching first db rows entries
        "id",
    )
    count = len(labels)
    with connection.cursor() as cur:
        cur.execute(SELECT["IMAGE_FOR_PLACE"], id=place_id)

        for row in cur.fetchall():
            yield {k: v for k, v in zip(labels, row[:count])}


def get_template(connection, template_type):
    with connection.cursor() as cur:
        cur.execute(SELECT["TEMPLATE"], type=template_type)
        return cur.fetchone()


def get_image(connection, id_image):
    connection.outputtypehandler = output_type_handler
    with connection.cursor() as cur:
        cur.execute(SELECT["IMAGE"], id=id_image)
        return cur.fetchone()


def get_static_data(connection, name):
    labels = (  # matching first db rows entries
        "varchar_value", "date_value", "number_value"
    )
    count = len(labels)
    with connection.cursor() as cur:
        cur.execute(SELECT["STATIC_DATA"], name=name)
        row = cur.fetchone()
        return {k: v for k, v in zip(labels, row[:count])}


def update_last_access(connection, date):
    with connection.cursor() as cur:
        cur.execute(UPDATE["LAST_ACCESS"], date_value=date)
        connection.commit()
