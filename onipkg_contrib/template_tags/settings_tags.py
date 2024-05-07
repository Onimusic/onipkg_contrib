from django import template
from django.contrib.staticfiles.storage import staticfiles_storage


register = template.Library()


@register.inclusion_tag('admin/changelog.html')
def get_changelog():
    import json
    json_data = open(staticfiles_storage.path('changelog.json'))
    changelog_dict = json.load(json_data)  # deserialises it
    json_data.close()
    return {'changelog': changelog_dict}


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
