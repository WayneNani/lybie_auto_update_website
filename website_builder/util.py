import os

import git
import pysftp

import website_builder.oracle_connector as oracle_connector
import website_builder.file_builder as file_builder
from website_builder.util_print import print_success, print_status


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


def save_files_to_disk(images, base_path):
    images_file_names = []
    for image in images:
        image_binary = oracle_connector.get_image(image["id"])
        images_file_names.append(image["file_name"])

        save_file_to_disk(image["file_name"], image_binary, base_path)

    return images_file_names


def save_file_to_disk(image_name, image_data, base_path):
    file_builder.write_file(
        path=os.path.join(base_path, 'static', 'img', 'portfolio', image_name),
        mode='wb',
        content=image_data
    )


