from django.utils.html import format_html
from django.template import Template
from django.http import JsonResponse

class Style():
    global ButtonStyle, InputStyle, RowCellStyle, RowStyle ,leftSpace, globalSpacing, TextAlignCenter, cellSpacing
    ButtonStyle     = "w3-cell w3-button w3-blue w3-round-large "
    globalSpacing   = "w3-margin"
    cellSpacing     = "w3-padding"
    leftSpace       = "w3-margin-left"
    TextAlignCenter = "w3-center"
    InputStyle      = "w3-card"
    RowCellStyle    = "w3-cell-row"
    RowStyle        = "w3-cell"
    

class appControls():
    def getInputFields():
        methods_list = [method for method in dir(base) if callable(getattr(base, method)) and not method.startswith("__")]
        return(methods_list)

class base(Style):

    def textInput(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                      <label class="w3-cell" for="{label}">{label}</label> \
         <input class="w3-input w3-border w3-round-large" name="{label}" type="text" {attr}>\
                  </div>')
        return t

    def textInput2(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="w3-cell-row {globalSpacing}"> \
                      <label class="w3-cell" for="{label}">{label}</label>\
                      <input class="w3-cell w3-input w3-border w3-round-large" name="{label}" type="text" {attr}>\
                  </div>')
        return t

    def container(*args,**kwargs):
        label = kwargs.get('label','') 
        attr = kwargs.get('attr','')
        children = kwargs.get('children','')
        t=format_html(f'<div class="w3-container w3-row-cell{globalSpacing}" {attr} >{children}</div>')
        return t

    def columnContainer(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        children = kwargs.get('children','')
        t=format_html(f'<div class="w3-container {RowStyle}{globalSpacing}" {attr}>{children}</div>')
        return t

    def modalContainer(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        children = kwargs.get('children','')
        t=format_html(f'<div class="w3-modal" id="modal" {attr}>\
            <div class="w3-modal-content w3-round-large w3-row-cell w3-display-middle {globalSpacing}" style="width:40%;">\
                {children}\
            </div>\
        </div>')
        return t

    def fieldsetContainer(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        children = kwargs.get('children','')
        t=format_html(f'<fieldset {InputStyle}{attr}><legend>{label}</legend>{children}</fieldset>')
        return t

    def form(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        children = kwargs.get('children','')
        t=format_html(f'<form autocomplete="on" {attr}>\
                      {children}\
                      </form>')
        return t

    def button(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<button class="{ButtonStyle}{globalSpacing}" type="{label}" value="{label}" name="{label}" {attr}>{label}</button>')
        return t

    def radio(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                           <label class="w3-padding-16" for="{label}">{label}</label> \
                           <input type="radio" name="{label}" class="{leftSpace}{RowStyle}{InputStyle}" {attr}/> \
                           </div>')
        return t

    def checkbox(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{cellSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="checkbox" name="{label}" class="{leftSpace}{RowStyle}{InputStyle}" {attr}/> \
                         </div>')
        return t

    def list(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        children = kwargs.get('children','')
# itemlist = ["company1","company2","company3"]
        option = ""
        if(len(children)!= 0):
          for item in children:
          # for item in itemlist:
            option += f'<option>{item}</option>'

        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <div class="w3-dropdown-hover">\
                             <select name="{label}" class="w3-button {leftSpace}{RowStyle}{InputStyle}" {attr}>{option}</select>\
                         </div>\
                      </div>')
        return t
         
    def color(*args,**kwargs):
       label = kwargs.get('label','')
       attr = kwargs.get('attr','')
       t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="{label}">{label}</label> \
                        <input type="color" name="{label}"  class="{leftSpace}{InputStyle}"/> \
                        </div>')
       return t

    def date(*args,**kwargs):
       label = kwargs.get('label','')
       attr = kwargs.get('attr','')
       t=format_html(f'<div class="{globalSpacing}"> \
                        <label class="" for="{label}">{label}</label> \
                        <input type="date" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                        </div>')
       return t

    def datetime(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="datetime-local" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def email(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="email" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def files(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="file" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def image(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                    <input type="image" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def month(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="month" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def number(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="number" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def password(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="password" name="{label}"  class="{RowStyle}{InputStyle}w3-cell w3-input w3-border w3-round-large"/> \
                         </div>')
        return t

    def range(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="range" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def reset(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="reset" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def search(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="search" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def submit(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="submit" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def tel(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="tel" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def time(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="time" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def url(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="url" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t

    def week(*args,**kwargs):
        label = kwargs.get('label','')
        attr = kwargs.get('attr','')
        t=format_html(f'<div class="{globalSpacing}"> \
                         <label class="" for="{label}">{label}</label> \
                         <input type="week" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                         </div>')
        return t
