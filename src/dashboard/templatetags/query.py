from django import template

register = template.Library()

@register.assignment_tag
def query(qs, **kwargs): # Only one argument
    for q in qs:
        reset_date = q.user.dashboard.reset_date
    # return qs.filter(timestamp__gte=reset_date, **kwargs)
    return qs.filter(**kwargs)
