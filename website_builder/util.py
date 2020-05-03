import json
import os

import git
from termcolor import colored
import pysftp

import website_builder.oracle_connector as oracle_connector
import website_builder.file_builder as file_builder


def write_files_to_sftp(server, user, password):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load('known_hosts')

    with pysftp.Connection(server,
                           username=user, password=password,
                           cnopts=cnopts) as sftp:
        sftp.chdir('places-unity')

        print_status('Lade Dateien auf den Server...')

        sftp.put_r('public', '.', preserve_mtime=True)

        print_success('Dateien erfolgreich hochgeladen!')


def initiate_git_repo(base_path):
    repository = git.Repo(base_path)

    # Get latest git changes and set HEAD to last commit on master
    repository.heads.master.checkout()
    repository.remote(name='origin').pull()
    repository.head.reset(index=True, working_tree=True)
    repository.git.clean('-f')

    return repository


def push_git_new_branch(repository, branch_name, commit_message, author):
    repository.create_head(branch_name).checkout()
    repository.git.commit('-m', commit_message, author=author)
    repository.git.push('--set-upstream', 'origin', branch_name)


def check_git_for_matching_branch(repo):
    for head in repo.heads:
        head.checkout()
        if not repo.is_dirty():
            return True
    return False


def print_error(message):
    print(colored(message, 'red'))


def print_success(message):
    print(colored(message, 'green'))


def print_status(message):
    print(colored(message, 'blue', attrs=['blink']), end='\r')


def save_files_to_disk(images, base_path, db_connection):
    images_file_names = []
    for image in images:
        image_row = oracle_connector.get_image(db_connection, image["id"])
        images_file_names.append(image_row[0])

        save_file_to_disk(image_row[0], image_row[1], base_path)

    return images_file_names


def save_file_to_disk(image_name, image_data, base_path):
    file_builder.write_file(
        path=os.path.join(base_path, 'static', 'img', 'portfolio', image_name),
        mode='wb',
        content=image_data
    )


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
