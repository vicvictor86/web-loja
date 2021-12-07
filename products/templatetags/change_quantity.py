from django import template

register = template.Library()
def change_quantity(variable, quantity):
    variable = quantity
    return variable

register.filter('change_quantity', change_quantity)