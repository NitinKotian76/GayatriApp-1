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
  # methods_list = [method for method in dir(base) if callable(getattr(base, method)) and not method.startswith("__")]
  # print(methods_list)
  return "hello"
 def items(item):
  match item:
    case 'button':
        # button(children)
        pass
    case 'checkbox':
        pass
    case 'color':
        pass

    case 'columnContainer':
        pass

    case 'container':
        pass

    case 'date':
        pass

    case 'datetime':
        pass

    case 'email':
        pass

    case 'fieldsetContainer':
        pass

    case 'files':
        pass

    case 'image':
        pass

    case 'list':
        pass

    case 'modalContainer':
        pass

    case 'month':
        pass

    case 'number':
        pass

    case 'password':
        pass

    case 'radio':
        pass

    case 'range':
        pass

    case 'reset':
        pass

    case 'search':
        pass

    case 'submit':
        pass

    case 'tel':
        pass

    case 'textInput':
        pass

    case 'textInput2':
        pass

    case 'time':
        pass

    case 'url':
        pass

    case 'week':
        pass

class base(Style):


 def textInput(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                  <label class="w3-cell" for="{label}">{label}</label> \
     <input class="w3-input w3-border w3-round-large" name="{label}" type="text" {attr}>\
              </div>')
  return t

 def textInput2(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="w3-cell-row {globalSpacing}"> \
                  <label class="w3-cell" for="{label}">{label}</label>\
                  <input class="w3-cell w3-input w3-border w3-round-large" name="{label}" type="text" {attr}>\
              </div>')
  return t

 def container(children, *args, **kwargs): 
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="w3-container w3-row-cell{globalSpacing}">{children}</div>')
  return t

 def columnContainer(children, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="w3-container {RowStyle}{globalSpacing}">{children}</div>')
  return t

 def modalContainer(children, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="w3-modal" id="modal" {attr}>\
        <div class="w3-modal-content w3-round-large w3-row-cell w3-display-middle {globalSpacing}" style="width:40%;">\
            {children}\
        </div>\
    </div>')
  return t

 def fieldsetContainer(label,children,*args,**kwargs):
     attr = kargs.get('attr','')
     t=format_html(f'<fieldset><legend>{label}</legend>{children}</fieldset>')

 def button(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<button class="{ButtonStyle}{globalSpacing}" for="{label}"{attr}>{label}</button>')
  return t

 def radio(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="w3-padding-16" for="{label}">{label}</label> \
                     <input type="radio" name="{label}" class="{leftSpace}{RowStyle}{InputStyle}"/> \
                     </div>')
  return t
 
 def checkbox(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="checkbox" name="{label}" class="{leftSpace}{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def list(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  itemlist = ["company1","company2","company3"]
  option = ""
  for item in itemlist:
    option += f'<option>{item}</option>'

  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <div class="w3-dropdown-hover">\
                         <select name="{label}" class="w3-button {leftSpace}{RowStyle}{InputStyle}">{option}</select>\
                     </div>\
                  </div>')
  return t
 
 def color(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="color" name="{label}"  class="{leftSpace}{InputStyle}"/> \
                     </div>')
  return t

 def date(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="date" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def datetime(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="datetime-local" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def email(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="email" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def files(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="file" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def image(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                <input type="image" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def month(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="month" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def number(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="number" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def password(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="password" name="{label}"  class="{RowStyle}{InputStyle}w3-cell w3-input w3-border w3-round-large"/> \
                     </div>')
  return t

 def range(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="range" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def reset(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="reset" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def search(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="search" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def submit(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="submit" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def tel(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="tel" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def time(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="time" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def url(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="url" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t

 def week(label, *args, **kwargs):
  attr = kwargs.get('attr','')
  t=format_html(f'<div class="{globalSpacing}"> \
                     <label class="" for="{label}">{label}</label> \
                     <input type="week" name="{label}"  class="{RowStyle}{InputStyle}"/> \
                     </div>')
  return t
    

