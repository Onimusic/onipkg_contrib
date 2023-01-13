from django.utils.html import format_html


def return_mark_safe(string):
    return format_html(string.replace("{", "{{").replace("}", "}}"))


def remove_parameters_and_dash(string):
    dash_location = string.find('/')
    if dash_location >= 0:
        string = string[:dash_location]
    params_locations = string.find('?')
    if params_locations >= 0:
        string = string[:params_locations]
    return string
