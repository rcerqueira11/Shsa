from django import template
from django.conf import settings

register = template.Library()

primera_colu =[1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91, 94, 97, 100, 103, 106, 109, 112, 115, 118, 121, 124, 127, 130, 133, 136, 139, 142, 145, 148]
segunda_colu =[2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 89, 92, 95, 98, 101, 104, 107, 110, 113, 116, 119, 122, 125, 128, 131, 134, 137, 140, 143, 146, 149]
tercera_colu =[3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 129, 132, 135, 138, 141, 144, 147, 150]


@register.filter(name='primera_col')
def primera_col(indice):
    return indice in primera_colu

@register.filter(name='segunda_col')
def segunda_col(indice):
    return indice in segunda_colu

@register.filter(name='tercera_col')
def tercera_col(indice):
    return indice in tercera_colu

@register.assignment_tag(name='input_content')
def input_content(form_data, key):
    content = {
        'value': '',
        'error': ''
    }

    if key in form_data.keys():
        content['value'] = form_data[key][0]
        content['error'] = form_data[key][1]

    return content