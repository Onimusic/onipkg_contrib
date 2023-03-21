def get_errors_messages_html(errors) -> str:
    """Retorna um código html com uma lista ordenada de erros ou n/a
    """
    if errors is not None and errors != "":
        errors = str(errors).split("|")
        from django.utils.html import format_html
        return format_html('<br><ol>{}</ol>'.format("".join(["<li>{}</li>".format(error) for error in errors])))
    else:
        return "n/a"
