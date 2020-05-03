import os
import datetime

import website_builder.file_builder as file_builder
import website_builder.util as util
import website_builder.oracle_connector as oc

CONFIG = util.load_config(os.path.join('website_builder', 'credentials.json'))

GIT_AUTHOR_EMAIL = CONFIG.get("GIT_EMAIL")
HUGO_BASE = CONFIG.get("HUGO_BASE")
COMMIT_MESSAGE_TODO = 'Some fine-tuning needed...'
DEFAULT_COMMIT_MESSAGE = 'Automatic update of places and sidebar data: '

errors = False
many_images = False

os.chdir(HUGO_BASE)

repo = util.initiate_git_repo(HUGO_BASE)

db_connect_string = util.db_connection_string(CONFIG)
# Establish connection to Oracle DB
with oc.connect(db_connect_string) as con:
    last_access = oc.get_static_data(con, 'LAST_ACCESS')["date_value"]

    # Generate and write config.toml to disk
    config_content = file_builder.get_config_file_content(
        sidebar_text_de=oc.get_static_data(con, 'VORSTELLUNGSTEXT_DE')["varchar_value"],
        sidebar_text_en=oc.get_static_data(con, 'VORSTELLUNGSTEXT_EN')["varchar_value"],
        template=oc.get_template(con, 'CONFIG')[0])

    try:
        file_builder.write_file(path=os.path.join(HUGO_BASE, 'config.toml'),
                                mode='w', content=config_content)
        util.print_success('config.toml erfolgreich gespeichert')
    except Exception as e:
        util.print_error('Fehler beim speichern von config.toml')
        errors = True

    # Generate and write sidebar.html to disk
    location = file_builder.get_sidebar_file_content(
        location=oc.get_static_data(con, 'AUFENTHALTSORT')["varchar_value"],
        travel_date=oc.get_static_data(con, 'REISEDATUM')["varchar_value"],
        template=oc.get_template(con, 'SIDEBAR')[0])

    try:
        file_builder.write_file(path=os.path.join(HUGO_BASE, 'themes', 'hugo-creative-portfolio-theme',
                                                  'layouts', 'partials', 'sidebar.html'),
                                mode='w', content=location)
        util.print_success('sidebar.html erfolgreich gespeichert')
    except Exception as _:
        util.print_error('Fehler beim speichern von sidebar.html')
        errors = True

    # Get new places and create files and images
    for place in oc.get_place_data(con, last_access):
        images_file_names = []
        place_template = oc.get_template(con, 'PLACE')[0]

        # Save Thumbnail
        if place["id_thumbnail"]:
            thumbnail = oc.get_image(con, place["id_thumbnail"])
            try:
                util.save_file_to_disk(thumbnail[0], thumbnail[1], HUGO_BASE)
            except Exception as e:
                util.print_error(f'Fehler beim speichern von {thumbnail[0]}')
                print(e)
                errors = True

            thumbnail_name = thumbnail[0]
        else:
            thumbnail_name = ''
            util.print_error(f'Kein Thumbnail für "{place["place_name"]}" angegeben!')

        # Save Images referenced in the text
        try:
            images_file_names = util.save_files_to_disk(
                oc.get_images_for_place(con, place["id"]), HUGO_BASE, con)
        except Exception as _:
            util.print_error(f'Fehler beim speichern der Bilder von "{place["place_name"]}"')
            errors = True

        if len(images_file_names) > 1:
            many_images = True

        place_template = oc.get_template(con, 'PLACE')[0]

        place_content_de = file_builder.get_place_file_content(
            text=place["text_de"],
            location=place["location_de"],
            creation_date=place["creation_date"].strftime("%Y-%m-%d"),
            thumbnail=thumbnail_name,
            template=place_template,
            images=images_file_names)

        place_content_en = file_builder.get_place_file_content(
            text=place["text_en"],
            location=place["location_en"],
            creation_date=place["creation_date"].strftime("%Y-%m-%d"),
            thumbnail=thumbnail_name,
            template=place_template,
            images=images_file_names)

        try:
            file_builder.write_file(
                path=os.path.join(HUGO_BASE, 'content', 'portfolio', place["place_name"] + '.de.md'),
                mode='w', content=place_content_de)

            file_builder.write_file(
                path=os.path.join(HUGO_BASE, 'content', 'portfolio', place["place_name"] + '.md'),
                mode='w', content=place_content_en)
        except Exception as _:
            util.print_error(f'Fehler beim speichern von {place["place_name"]}')
            errors = True

    # oracle_connector.update_last_access(con, datetime.datetime.now())

repo.git.add(all=True)

# Check if files have been changed/added and no errors occured
if repo.is_dirty() and not errors:
    # If more than one image is included I have to manually fix the manually so I need a branch to work in
    if many_images:
        found_matching_branch = False

        if len(repo.heads) > 1:
            # Check if there's a HEAD that already contains all the changes...
            found_matching_branch = util.check_git_for_matching_branch(repo)

            if not found_matching_branch:
                new_branch_name = f'new_place_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")}'
                util.push_git_new_branch(repo, new_branch_name, DEFAULT_COMMIT_MESSAGE + COMMIT_MESSAGE_TODO,
                                         GIT_AUTHOR_EMAIL)
        else:
            new_branch_name = f'new_place_{datetime.datetime.now().strftime("%Y_%m_%d")}'
            util.push_git_new_branch(repo, new_branch_name, DEFAULT_COMMIT_MESSAGE + COMMIT_MESSAGE_TODO,
                                     GIT_AUTHOR_EMAIL)

        repo.heads.master.checkout()
        util.print_success('Das wars mit deiner Arbeit...jetzt ist Jakob dran ;)')
    else:
        custom_commit_message = input('Was hast du an der Seite verändert?\n')

        # Build Hugo site
        os.system('hugo')

        repo.git.commit('-m', DEFAULT_COMMIT_MESSAGE + custom_commit_message, author=GIT_AUTHOR_EMAIL)
        repo.remotes.origin.push()

        # Upload changes to the website
        util.write_files_to_sftp(
            CONFIG.get('SFTP_SERVER'), CONFIG.get('SFTP_USER'), CONFIG.get('SFTP_PASSWORD'))

elif errors:
    util.print_error('Es sind einige Fehler aufgetreten. Bitte sag Jakob bescheid :(')
else:
    print('Es wurden keine Änderungen vorgenommen...')
