from django.utils.html import format_html
from django.template import Template
from django.http import JsonResponse

class Style():
    global ButtonStyle, InputStyle,RowCellStyle, RowStyle ,leftSpace, globalSpacing,TextAlignCenter, cellSpacing
    ButtonStyle = " w3-cell w3-button w3-blue w3-round-large"
    globalSpacing = " w3-margin-left w3-margin-top "
    cellSpacing = "w3-padding"
    leftSpace = "w3-margin-left"
    TextAlignCenter = "w3-center"
    InputStyle = " w3-card "
    RowCellStyle = "w3-cell-row"
    RowStyle = " w3-cell "
    
class base(Style):
    
    def form(children):
        t=format_html(f'<form action="" method="post" class="w3-container w3-cell-row">{children}</form>')
        return t

    def text_input():
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="w3-cell" for="">Label</label> \
                        <input class="w3-input w3-border w3-round-large" type="text">\
                    </div>')
        return t

    def text_input2():
        t=format_html(f'<div class="w3-cell-row {globalSpacing}"> \
                        <label class="w3-cell" for="">Label</label>\
                        <input class="w3-cell w3-input w3-border w3-round-large" type="text">\
                    </div>')
        return t
    def Container(Children):
        t=format_html(f'<div class="w3-container w3-row-cell{globalSpacing}">{Children}</div>')
        return t

    def columnContainer(Children):
        t=format_html(f'<div class="w3-container {RowStyle}{globalSpacing}">{Children}</div>')
        return t

    def button(label):
        t=format_html(f'<button class="{ButtonStyle}{globalSpacing}">{label}</button>')
        return t

    def radio(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="w3-padding-16" for="">{label}</label> \
                        <input type="radio" class="{leftSpace}{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    
    def checkbox(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="checkbox" class="{leftSpace}{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    
    def color(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="color" class="{leftSpace}{InputStyle}"/> \
                        </div>')
        return t
    def date(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="date" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def datetime(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="datetime-local" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def email(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="email" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def files(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="file" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def image(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="image" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def month(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="month" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def number(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="number" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def password(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="password" class="{leftSpace}{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def range(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="range" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def reset(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="reset" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def search(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="search" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def submit(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="submit" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def tel(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="tel" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def time(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="time" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def url(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="url" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    def week(label):
        t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="">{label}</label> \
                        <input type="week" class="{RowStyle}{InputStyle}"/> \
                        </div>')
        return t
    
class appControls(Style):
    
    def add():
        t=format_html(f'<div class="w3-cell-row w3-margin-top">\
                            <div class=" w3-dropdown-click w3-cell" style="width:80%">\
                                <button onclick="Click()" class="addbtn w3-cell-row w3-button w3-blue">+</button>\
                                <div id="inputlist" class="w3-dropdown-content w3-bar-block w3-border">\
                                    <div >\
                                        <a href="#" class="w3-bar-item w3-button">Link 1</a>\
                                        <a href="#" class="w3-bar-item w3-button">Link 2</a>\
                                        <a href="#" class="w3-bar-item w3-button">Link 3</a>\
                                    </div>\
                                </div>\
                            </div>\
                            <div class="w3-cell" style="width:20%">\
                            <button class="w3-cell-row w3-button w3-blue">+</button>\
                            </div>\
                        </div>\
                        ')
        return t
    
   