def get_errors_messages_html(errors) -> str:
    """Retorna um código html com uma lista ordenada de erros ou n/a
    """
    if errors is None or errors == "":
        return "n/a"
    errors = str(errors).split("|")
    from django.utils.html import format_html
    return format_html(
        f'<br><ol>{"".join([f"<li>{error}</li>" for error in errors])}</ol>'
    )
