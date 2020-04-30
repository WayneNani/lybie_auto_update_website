def get_place_file_content(text, location, creation_date, thumbnail, template,
                           images):
    place_content = template.replace('[TEXT]', text)
    place_content = place_content.replace('[LOCATION]', location)
    place_content = place_content.replace('[DATE]', creation_date)
    place_content = place_content.replace('[THUMBNAIL]', '/img/portfolio/' + thumbnail)

    image_string = ''

    for image in images:
        image_string += f'<img src="/img/portfolio/{image}" width=70% id="bildImText"/>\n'

    place_content = place_content.replace('[IMAGE]', image_string)

    return place_content


def get_sidebar_file_content(location, travel_date, template):
    if location.lower() == 'de':
        back = 'us'
    else:
        back = 'de'

    if travel_date:
        sidebar_content = template.replace('[LOCATION_EN]',
                                           f'<p class="sidebar-p" style="color:black;"><b>I am currently in </b> <img '
                                           f'class="sidebar-img" src=/img/{location.lower()}.gif></p><p '
                                           f'class="sidebar-p">I will be back in <img class="sidebar-img" src=/img/'
                                           f'{back}.gif> on {travel_date} </p>')

        sidebar_content = sidebar_content.replace('[LOCATION_DE]',
                                                  f'<p class="sidebar-p" style="color:black;"><b>Ich bin gerade in '
                                                  f'</b> <img class="sidebar-img" src=/img/'
                                                  f'{location.lower()}.gif></p><p class="sidebar-p">Ich komme zurück '
                                                  f'nach <img class="sidebar-img" src=/img/{back}.gif> am '
                                                  f'{travel_date}</p>')

    else:
        sidebar_content = template.replace('[LOCATION_EN]',
                                           f'<p class="sidebar-p" style="color:black;"><b>I am currently in </b> <img '
                                           f'class="sidebar-img" src=/img/{location.lower()}.gif></p>')

        sidebar_content = sidebar_content.replace('[LOCATION_DE]',
                                                  f'<p class="sidebar-p" style="color:black;"><b>Ich bin gerade in '
                                                  f'</b> <img class="sidebar-img" src=/img/'
                                                  f'{location.lower()}.gif></p>')

    return sidebar_content


def get_config_file_content(sidebar_text_de, sidebar_text_en, template):
    sidebar_text_de = sidebar_text_de.replace('\n', '</br>')
    sidebar_text_en = sidebar_text_en.replace('\n', '</br>')

    content = template.replace('[TEXT_EN]', sidebar_text_en)
    content = content.replace('[TEXT_DE]', sidebar_text_de)

    return content


def write_file(path, mode, content):
    file = open(path, mode)
    file.write(content)
    file.close()
