from django import template
register = template.Library()


@register.filter(name='add_attr')
def add_attr(field, css):
    print('here')
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')[0], d.split(':')[1]
            attrs[key] = val

    return field.as_widget(attrs=attrs)
