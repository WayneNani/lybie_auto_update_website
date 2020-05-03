import cx_Oracle
import datetime


def output_type_handler(cursor, name, defaultType, size, precision, scale):
    if defaultType == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, arraysize=cursor.arraysize)
    if defaultType == cx_Oracle.BLOB:
        return cursor.var(cx_Oracle.LONG_BINARY, arraysize=cursor.arraysize)


def connect(db_connect_string):
    return cx_Oracle.connect(db_connect_string, encoding="UTF-8")


def get_place_data(connection, last_access=datetime.datetime(1970, 1, 1,)):
    return_array = []
    with connection.cursor() as temp_cursor:
        temp_cursor.execute("""
            select p.ID, name, text_de, text_en, location_de,
                   location_en, creation_date, file_name, date_modified, i.ID
            from   places p
            left join images i ON p.THUMBNAIL = i.ID
            where date_modified > :last_access
            order by p.id asc""",
                            last_access=last_access)

        for row in temp_cursor.fetchall():
            temp_dict = {"id": row[0], "place_name": row[1], "text_de": row[2], "text_en": row[3],
                         "location_de": row[4], "location_en": row[5], "creation_date": row[6], "file_name": row[7],
                         "date_modified": row[8], "id_thumbnail": row[9]}
            return_array.append(temp_dict)

        return return_array


def get_images_for_place(connection, place_id):
    return_array = []
    with connection.cursor() as cur:
        cur.execute("""
                SELECT ID_IMAGE
                FROM PLACE_IMAGE_MAPPING
                WHERE ID_PLACE = :id""",
                    id=place_id)

        for row in cur.fetchall():
            temp_dict = {"id": row[0]}
            return_array.append(temp_dict)

        return return_array


def get_template(connection, template_type):
    with connection.cursor() as cur:
        cur.execute(f"""
                select template_content
                from templates
                where name = :type""",
                    type=template_type)

        row = cur.fetchone()
        return row


def get_image(connection, id_image):
    connection.outputtypehandler = output_type_handler
    with connection.cursor() as cur:
        cur.execute("""
                select file_name, blob_content
                from images
                where id = :id""",
                    id=id_image)

        row = cur.fetchone()
        return row


def get_static_data(connection, name):
    with connection.cursor() as cur:
        cur.execute("""
                select varchar_value, date_value, number_value
                from static_content
                where name = :name""",
                    name=name)
        row = cur.fetchone()
        temp_dict = {"varchar_value": row[0], "date_value": row[1], "number_value": row[2]}

        return temp_dict


def update_last_access(connection, date):
    with connection.cursor() as cur:
        cur.execute("""
                update static_content
                set date_value = :date_value
                where name = 'LAST_ACCESS'""",
                    date_value=date)

        connection.commit()
