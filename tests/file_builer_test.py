import website_builder.file_builder as fb


def test_get_config_file():
    test_de = 'DE\r\nDE'
    test_en = 'EN\r\nEN'
    template = 'Test1: [TEXT_DE]\nTest2: [TEXT_EN]'

    assert fb.get_config_file_content(test_de, test_en, template) == 'Test1: DE<br>DE\nTest2: EN<br>EN'


def test_sidebar_with_travel_date():
    reference = '<p class="sidebar-p" style="color:black;"><b>I am currently in </b> <img ' \
                'class="sidebar-img" src=/img/{0}.gif></p><p class="sidebar-p">I will be back in <img ' \
                'class="sidebar-img" src=/img/{1}.gif> on {2} </p>\n<p class="sidebar-p" style="color:black;"><b>Ich ' \
                'bin gerade in </b> <img class="sidebar-img" src=/img/{3}.gif></p><p class="sidebar-p">Ich komme ' \
                'zurück nach <img class="sidebar-img" src=/img/{4}.gif> am {5}</p>'

    thing = '12.12.12'
    template = '[LOCATION_EN]\n[LOCATION_DE]'
    data = {
        ('DE', thing,): ('de', 'us', thing, 'de', 'us', thing),
        ('US', thing,): ('us', 'de', thing, 'us', 'de', thing),
    }
    retrieve = fb.get_sidebar_file_content
    for keys, out_params in data.items():
        assert retrieve(*keys, template) == reference.format(*out_params)


def test_sidebar_no_travel_date():
    reference = (
        '<p class="sidebar-p" style="color:black;"><b>I am currently in </b> <img'
        ' class="sidebar-img" src=/img/{0}.gif></p>\n<p class="sidebar-p" style="color:black;"><b>Ich'
        ' bin gerade in </b> <img class="sidebar-img" src=/img/{1}.gif></p>')

    thing = None
    template = '[LOCATION_EN]\n[LOCATION_DE]'
    data = {
        ('DE', thing,): ('de', 'de'),
        ('US', thing,): ('us', 'us'),
    }
    retrieve = fb.get_sidebar_file_content
    for keys, out_params in data.items():
        assert retrieve(*keys, template) == reference.format(*out_params)


def test_place_content():
    data = {
        'text': 'testText',
        'location': 'testLocation',
        'date': 'testDate',
        'thumbnail': 'thumb',
        'template': '[TEXT]\n[LOCATION]\n[DATE]\n[THUMBNAIL]\n[IMAGE]',
        'image': ['image01'],
    }
    retrieve = fb.get_place_file_content
    assert retrieve(*data.values()) == (
        '{text}\n{location}\n{date}\n/img/portfolio/thumb'
        '\n<img src="/img/portfolio/image01" width=70% id="bildImText"/>\n'
    ).format(**data)
