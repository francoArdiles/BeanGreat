from django.template import Library

register = Library()


@register.filter(name='edit_field')
def edit_field(field, args):
    attributes = {}
    arg_list = [arg.strip().split('|') for arg in args.split('&')]
    for attrs in arg_list:
        attributes[attrs[0]] = attrs[1]

    return field.as_widget(attrs=attributes)
