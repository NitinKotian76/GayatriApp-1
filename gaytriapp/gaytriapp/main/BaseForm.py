from django.utils.html import format_html
from django.template import Template


def form(children):
    t=format_html("<form action='' method='post'>{}</form>",children)
    return t

def text_input():
    t=format_html('<div{}> \
                    <label class="" for="">Label</label> \
                    <input class="w3-input w3-border w3-round-large" type="text">\
                </div>')
    return t

def text_input2():
    t=format_html('<div class="w3-cell-row"> \
                    <label class="w3-cell" for="">Label</label>\
                    <input class="w3-cell w3-input w3-border w3-round-large" type="text">\
                </div>')
    return t
def Container():
    
    t=format_html('<div class="w3-container w3-cell"></div>')
    return t