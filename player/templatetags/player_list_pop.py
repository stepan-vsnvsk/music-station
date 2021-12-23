from django import template

register = template.Library()

@register.filter
def player_list_pop(sequence):         
    # Return and remove first item in a list 
    if sequence:               
        return sequence.pop(0)



