from django import template

register = template.Library()

@register.filter
def get_match_value(value, student_pk):
    match_value = value[student_pk]
    return match_value
