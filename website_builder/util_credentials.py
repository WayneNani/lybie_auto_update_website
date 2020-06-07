import json
import os

from website_builder.util_print import print_error


def path_to_config(folder=None):
    """Derive path to the json file for credentials loading."""
    if folder is None:
        folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, 'credentials.json')


def load_config(json_path=None):
    """Load credentials from path to json file."""
    if json_path is None:
        json_path = path_to_config()
    try:
        return json.load(open(json_path), encoding='utf-8')
    except FileNotFoundError as e:
        print_error('"credentials.json" konnte nicht gefunden werden...')
        return {}


def db_connection_string(credentials=None):
    """Build the db connection string either from env vars or from json file."""
    if credentials is None:
        credentials = load_config()
    return (
        f'{credentials.get("ORACLE_DB_USER")}'
        f'/{credentials.get("ORACLE_DB_PASSWORD")}'
        f'@{credentials.get("ORACLE_DB_IP")}:1539/xepdb1'
    )


def webservice_url(credentials=None):
    if credentials is None:
        credentials = load_config()
    return credentials.get("WEBSERVICE_BASE_URL")