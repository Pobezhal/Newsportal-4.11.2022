from django import template


register = template.Library()


Slovechki = [
    'Слеш',
    'Мбаппе'
]

@register.filter()
def cenzura(value):

    for word in Slovechki:
        value = value.replace(word, '*' * len(word))
    return value