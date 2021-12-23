from django import template

register = template.Library()

@register.filter
def player_index(indexable, i):    
    # return [i]
    if indexable:
        return indexable[i]

 
