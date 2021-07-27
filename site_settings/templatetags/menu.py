from django import template

from home.models import HomePage

register = template.Library()


items = HomePage.objects.first().get_children().live().public().in_menu()


# Advert snippets
@register.inclusion_tag('site_settings/tags/menu_items.html', takes_context=True)
def menu_items(context):
    return {
        'menu_items': items,
        'request': context['request'],
    }