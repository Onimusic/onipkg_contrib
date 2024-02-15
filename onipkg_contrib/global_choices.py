def font_types_list(for_choices=False) -> tuple:
    """Return a tuple of supported google font types.

    :param for_choices:
    :return: A full tuple of font objects or a tuple of ((key1, name1),(key2, name2).....(keyN, nameN))
    """
    #
    fonts = (
        {'name': 'Open Sans',
         'details': {'url': '<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">',
                     'css': 'font-family: \'Open Sans\', sans-serif'}},
        {'name': 'Major Mono Display',
         'details': {'url': '<link href="https://fonts.googleapis.com/css?family=Major+Mono+Display" rel="stylesheet">',
                     'css': 'font-family: \'Major Mono Display\', monospace'}},
        {'name': 'Roboto',
         'details': {'url': '<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">',
                     'css': 'font-family: \'Roboto\', sans-serif'}},
        {'name': 'Lato',
         'details': {'url': '<link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet">',
                     'css': 'font-family: \'Lato\', sans-serif'}},
        {'name': 'Montserrat',
         'details': {'url': '<link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">',
                     'css': 'font-family: \'Montserrat\', sans-serif'}},
        {'name': 'Source Sans Pro', 'details': {
            'url': '<link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro" rel="stylesheet">',
            'css': 'font-family: \'Source Sans Pro\', sans-serif'}},
        {'name': 'Oswald',
         'details': {'url': '<link href="https://fonts.googleapis.com/css?family=Oswald" rel="stylesheet">',
                     'css': 'font-family: \'Oswald\', sans-serif'}},
        {'name': 'Raleway',
         'details': {'url': '<link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">',
                     'css': 'font-family: \'Raleway\', sans-serif'}})

    return (
        ((str(key), item['name']) for key, item in enumerate(fonts))
        if for_choices
        else fonts
    )


def get_font_choices() -> tuple:
    """Font CSS to be used on templates. Defaults to Open Sans.
    """
    return font_types_list(True)


def _get_font_details(font_id: int = 0, item: str = 'url') -> str:
    """Private method. Get font details. Defaults to Open Sans.

    Used to reuse code in this file.

    :param font_id:
    :param item: item inside details to be returned
    """
    # if font_id is not on the list, defaults to opensans
    fonts_list = font_types_list()
    font_id = font_id if len(fonts_list) - 1 >= font_id else 0
    return fonts_list[font_id]['details'][item]


def get_font_url(font_id: int = 0) -> str:
    """Font CSS to be used on templates. Defaults to Open Sans.

    :param font_id:
    """
    return _get_font_details(font_id, 'url')


def get_font_style(font_id: int = 0) -> str:
    """Font CSS to be used on templates. Defaults to Open Sans.

    :param font_id:
    """
    return _get_font_details(font_id, 'css')


def simple_status_list(include_pendig: bool = False) -> tuple:
    """A list of 2 simple statuses. Success and error

    :return:
    """
    ret = [(str(70), 'Success'), (str(90), 'Error')]
    if include_pendig:
        ret[len(ret):] = [(str(1), 'Pending')]
    return tuple(ret)
