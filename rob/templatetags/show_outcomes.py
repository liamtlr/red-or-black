from django import template

register = template.Library()

@register.inclusion_tag('subtemplates/list_outcomes.html')
def show_outcomes(outcomes, outcome_string):
    outcomes = outcomes
    outcome_string = outcome_string
    return {'outcomes': outcomes, 'outcome_string': outcome_string}
