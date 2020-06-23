import json
import os


def path_to_config(folder=None):
    """Derive path to the json file for credentials loading."""
    if folder is None:
        folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, 'credentials.json')


def load_config(json_path=None):
    """Load credentials from path to json file."""
    if json_path is None:
        json_path = path_to_config()

    return json.load(open(json_path), encoding='utf-8')


def webservice_url(credentials=None):
    if credentials is None:
        credentials = load_config()
    return credentials.get("WEBSERVICE_BASE_URL")
