from django.utils.html import format_html
from django.template import Template
from django.http import JsonResponse
from django import forms


def getInputFields(object):
    methods_list = [
        method
        for method in dir(object)
        if callable(getattr(object, method)) and not method.startswith("__")
    ]
    return methods_list


class base:
    global ButtonStyle, InputStyle, RowCellStyle, RowStyle, leftSpace, globalSpacing, TextAlignCenter, cellSpacing
    ButtonStyle = " w3-cell w3-button w3-blue w3-round-large w3-ripple"
    globalSpacing = " w3-margin"
    cellSpacing = " w3-padding"
    leftSpace = " w3-margin-left"
    TextAlignCenter = " w3-center"
    InputStyle = " w3-card"
