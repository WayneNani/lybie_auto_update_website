import os
from datetime import datetime

import website_builder.util as util
import website_builder.oracle_connector as oc
import website_builder.util_credentials as util_credentials
from website_builder.util import handle_complex_changes, handle_simple_changes

CONFIG = util_credentials.load_config(os.path.join('website_builder', 'credentials.json'))

GIT_AUTHOR_EMAIL = CONFIG.get("GIT_EMAIL")
HUGO_BASE = CONFIG.get("HUGO_BASE")
SIDEBAR_DIR = os.path.join(HUGO_BASE, 'themes', 'hugo-creative-portfolio-theme',
                           'layouts', 'partials', 'sidebar.html')
COMMIT_MESSAGE_TODO = 'Some fine-tuning needed...'
DEFAULT_COMMIT_MESSAGE = 'Automatic update of places and sidebar data: '

connector = oc.Webservice(util_credentials.webservice_url(CONFIG))

os.chdir(HUGO_BASE)

repo = util.initiate_git_repo(HUGO_BASE)

last_access = datetime.strptime(connector.get_static_date('LAST_ACCESS'), '%Y-%m-%dT%H:%M:%SZ')

util.save_static_files(connector, HUGO_BASE, SIDEBAR_DIR)

more_than_one_image = util.save_updated_places(HUGO_BASE, last_access, connector)

connector.update_last_access(datetime.now())

repo.stage_everything()

# Check if files have been changed/added and no errors occured
if repo.is_dirty():
    if more_than_one_image:
        handle_complex_changes(repo, DEFAULT_COMMIT_MESSAGE + COMMIT_MESSAGE_TODO, GIT_AUTHOR_EMAIL)
    else:
        handle_simple_changes(repo, DEFAULT_COMMIT_MESSAGE, GIT_AUTHOR_EMAIL)

        # Build Hugo site
        util.build_hugo_site()

        # Upload changes to the website
        util.write_files_to_sftp(
            CONFIG.get('SFTP_SERVER'), CONFIG.get('SFTP_USER'), CONFIG.get('SFTP_PASSWORD'))
else:
    print('Es wurden keine Änderungen vorgenommen...')
