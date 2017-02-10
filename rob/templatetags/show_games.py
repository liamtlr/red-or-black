from django import template

register = template.Library()

@register.inclusion_tag('list_games.html')
def show_games(games, header, footer):
    games = games
    header = header
    footer = footer
    if header=='Games ready to join':
        link = 'set_stake'
    else:
        link ='view_game'
    return {'games': games, 'header': header, 'footer': footer, 'link': link}
