def get_place_file_content(
        text, location, creation_date, thumbnail, template, images):
    other_attributes = 'width=70% id="bildImText"'
    image_string = ''.join(f'<img src="/img/portfolio/{image}" {other_attributes}/>\n' for image in images)
    return (
        template
        .replace('[TEXT]', text)
        .replace('[LOCATION]', location)
        .replace('[DATE]', creation_date)
        .replace('[THUMBNAIL]', '/img/portfolio/' + thumbnail)
        .replace('[IMAGE]', image_string)
    )


def get_sidebar_file_content(location, travel_date, template):
    country = location.lower()
    other_country = 'us' if country == 'de' else 'de'

    if travel_date:
        return (
            template
            .replace(
                '[LOCATION_EN]',
                f'<p class="sidebar-p" style="color:black;"><b>I am currently in </b> <img '
                f'class="sidebar-img" src=/img/{country}.gif></p><p '
                f'class="sidebar-p">I will be back in <img class="sidebar-img" src=/img/'
                f'{other_country}.gif> on {travel_date} </p>')
            .replace(
                '[LOCATION_DE]',
                f'<p class="sidebar-p" style="color:black;"><b>Ich bin gerade in '
                f'</b> <img class="sidebar-img" src=/img/'
                f'{country}.gif></p><p class="sidebar-p">Ich komme zurück '
                f'nach <img class="sidebar-img" src=/img/{other_country}.gif> am '
                f'{travel_date}</p>')
        )

    else:
        return (
            template
            .replace(
                '[LOCATION_EN]',
                f'<p class="sidebar-p" style="color:black;"><b>I am currently in </b> <img '
                f'class="sidebar-img" src=/img/{country}.gif></p>')
            .replace(
                '[LOCATION_DE]',
                f'<p class="sidebar-p" style="color:black;"><b>Ich bin gerade in '
                f'</b> <img class="sidebar-img" src=/img/'
                f'{country}.gif></p>')
        )


def nl_to_br(text):
    """Htmlize line breaks."""
    return text.replace('\n', '<br>')


def get_config_file_content(sidebar_text_de, sidebar_text_en, template):
    """Htmlize line breaks of german and english side bar text in template."""
    return (template
            .replace('[TEXT_EN]', nl_to_br(sidebar_text_en))
            .replace('[TEXT_DE]', nl_to_br(sidebar_text_de))
            )


def write_file(path, mode, content):
    """Write content to file at path with mode."""
    with open(path, mode) as handle:
        handle.write(content)
