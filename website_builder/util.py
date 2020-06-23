import os
from datetime import datetime

import pysftp

from website_builder import file_builder as file_builder, util_print as util_print
from website_builder.util_print import print_success, print_status
import website_builder.pygit_extended as git_extended


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
    repository = git_extended.Repo(base_path)
    repository.get_latest_changes_on_master()

    return repository


def save_images_to_disk(connector, images, base_path):
    images_file_names = []
    for image in images:
        image_binary = connector.get_image(image["id"])
        images_file_names.append(image["file_name"])

        save_binary_file_to_disk(image["file_name"], image_binary, base_path)

    return images_file_names


def save_binary_file_to_disk(image_name, image_data, base_path):
    file_builder.write_binary_file(
        path=os.path.join(base_path, 'static', 'img', 'portfolio', image_name),
        content=image_data
    )


def build_hugo_site():
    os.system('hugo')


def save_static_files(connector, hugo_base, sidebar_dir):
    # Generate and write config.toml to disk
    config_content = file_builder.get_config_file_content(
        sidebar_text_de=connector.get_static_varchar('VORSTELLUNGSTEXT_DE'),
        sidebar_text_en=connector.get_static_varchar('VORSTELLUNGSTEXT_EN'),
        template=connector.get_template('CONFIG'))

    file_builder.write_text_file(path=os.path.join(hugo_base, 'config.toml'),
                                 content=config_content)
    util_print.print_success('config.toml erfolgreich gespeichert')

    # Generate and write sidebar.html to disk
    location = file_builder.get_sidebar_file_content(
        location=connector.get_static_varchar('AUFENTHALTSORT'),
        travel_date=connector.get_static_varchar('REISEDATUM'),
        template=connector.get_template('SIDEBAR'))

    file_builder.write_text_file(path=sidebar_dir, content=location)
    util_print.print_success('sidebar.html erfolgreich gespeichert')


def save_updated_places(hugo_base, last_access_date, connector):
    more_than_one_image = False
    # Get new places and create files and images
    for place in connector.get_place_data(last_access_date):
        place_template = connector.get_template('PLACE')

        # Save Thumbnail
        thumbnail_name = save_thumbnail(connector, hugo_base, place)

        # Save Images referenced in the text
        images_file_names = save_images_to_disk(connector, connector.get_images_for_place(place["id"]),
                                                hugo_base)

        more_than_one_image = len(images_file_names) > 1

        write_place_to_disk(hugo_base, images_file_names, place, place_template, thumbnail_name, 'de')
        write_place_to_disk(hugo_base, images_file_names, place, place_template, thumbnail_name, 'en')

    return more_than_one_image


def write_place_to_disk(hugo_base, images_file_names, place, place_template, thumbnail_name, location_identifier):
    if location_identifier == 'de':
        file_extension = '.de.md'
    else:
        file_extension = '.md'

    place_content = file_builder.get_place_file_content(
        text=place["text_" + location_identifier],
        location=place["location_" + location_identifier],
        creation_date=datetime.strptime(place["creation_date"], '%Y-%m-%dT%H:%M:%SZ').strftime("%Y-%m-%d"),
        thumbnail=thumbnail_name,
        template=place_template,
        images=images_file_names)

    file_builder.write_text_file(
        path=os.path.join(hugo_base, 'content', 'portfolio', place["place_name"] + file_extension),
        content=place_content)


def save_thumbnail(connector, hugo_base, place):
    if place["id_thumbnail"]:
        thumbnail = connector.get_image(place["id_thumbnail"])
        save_binary_file_to_disk(place['file_name'], thumbnail, hugo_base)
        thumbnail_name = place['file_name']
    else:
        thumbnail_name = ''
        util_print.print_error(f'Kein Thumbnail für "{place["place_name"]}" angegeben!')

    return thumbnail_name


def handle_complex_changes(repository, commit_message, author):
    if len(repository.heads) > 1:
        # Check if there's a HEAD that already contains all the changes...
        found_matching_branch = repository.check_git_for_matching_branch()

        if not found_matching_branch:
            new_branch_name = f'new_place_{datetime.now().strftime("%Y_%m_%d_%H_%M")}'
            repository.push_git_new_branch(new_branch_name, commit_message,
                                           author)
        else:
            new_branch_name = f'new_place_{datetime.now().strftime("%Y_%m_%d")}'
            repository.push_git_new_branch(new_branch_name, commit_message,
                                           author)

    util_print.print_success('Das wars mit deiner Arbeit...jetzt ist Jakob dran ;)')


def handle_simple_changes(repository, commit_message, author):
    custom_commit_message = input('Was hast du an der Seite verändert?\n')
    repository.git.commit('-m', commit_message + custom_commit_message, author=author)
    repository.remotes.origin.push()
