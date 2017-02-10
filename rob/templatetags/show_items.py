from django import template

register = template.Library()

@register.inclusion_tag('list_selections.html')
def show_items(colours, colour):
    items = colours
    colour = colour
    return {'items': items, 'colour': colour}
