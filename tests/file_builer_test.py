import website_builder.file_builder as fb


def test_get_config_file():
    test_de = 'DE\nDE'
    test_en = 'EN\nEN'
    template = 'Test1: [TEXT_DE]\nTest2: [TEXT_EN]'

    assert fb.get_config_file_content(test_de, test_en, template) == 'Test1: DE</br>DE\nTest2: EN</br>EN'


def test_sidebar_with_travel_date():
    template = '[LOCATION_EN]\n[LOCATION_DE]'

    reference = '<p class="sidebar-p" style="color:black;"><b>I am currently in </b> <img ' \
                'class="sidebar-img" src=/img/{0}.gif></p><p class="sidebar-p">I will be back in <img ' \
                'class="sidebar-img" src=/img/{1}.gif> on {2} </p>\n<p class="sidebar-p" style="color:black;"><b>Ich ' \
                'bin gerade in </b> <img class="sidebar-img" src=/img/{3}.gif></p><p class="sidebar-p">Ich komme ' \
                'zurück nach <img class="sidebar-img" src=/img/{4}.gif> am {5}</p>'

    assert fb.get_sidebar_file_content('DE', '12.12.12', template) == reference.format('de', 'us', '12.12.12',
                                                                                       'de', 'us', '12.12.12')

    assert fb.get_sidebar_file_content('US', '12.12.12', template) == reference.format('us', 'de', '12.12.12',
                                                                                       'us', 'de', '12.12.12')


def test_sidebar_no_travel_date():
    template = '[LOCATION_EN]\n[LOCATION_DE]'

    reference = '<p class="sidebar-p" style="color:black;"><b>I am currently in </b> <img ' \
                'class="sidebar-img" src=/img/{0}.gif></p>\n<p class="sidebar-p" style="color:black;"><b>Ich ' \
                'bin gerade in </b> <img class="sidebar-img" src=/img/{1}.gif></p>'

    assert fb.get_sidebar_file_content('DE', None, template) == reference.format('de', 'de')

    assert fb.get_sidebar_file_content('US', None, template) == reference.format('us', 'us')


def test_place_content():
    text = 'testText'
    location = 'testLocation'
    date = 'testDate'
    thumbnail = 'thumb'
    image = ['image01']

    template = '[TEXT]\n[LOCATION]\n[DATE]\n[THUMBNAIL]\n[IMAGE]'

    assert fb.get_place_file_content(text, location, date, thumbnail, template,
                                     image) == 'testText\ntestLocation\ntestDate' \
                                               '\n/img/portfolio/thumb\n<img ' \
                                               'src="/img/portfolio/image01" ' \
                                               'width=70% id="bildImText"/>\n'
