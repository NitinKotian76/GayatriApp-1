from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout
from django.views import View
import logging
from .cachestore import cachestore as cache
from .models import *
from .forms import *
from .formmod import DefaultForm as df
from .formmod import BaseForm as bf
from .dbmod import dbfunctions as db
from .reportmod import create_report as cr
from django.core.paginator import Paginator
from django.contrib import messages
# from .formmod.CrudForm import form_store_json


# NOTE: anything that is returned by the rendered template should be validated
# by the client and then the server

logger = logging.getLogger(__name__)
## COMMON ##


def login_user(request):
    if request.method == 'POST':
        form = bf.loginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            logger.debug("logged in")
            print(request.user.get_all_permissions())
            print(request.user.groups.all())
            return redirect("invoice:index")
    else:
        form = bf.loginForm()
        if not request.user.is_authenticated:
            logger.debug("login password or username failed")
    return render(request, "invoice/login.html", {"login": form, "messages": messages.get_messages(request)})


@login_required
def logout_user(request):
    logger.debug("logout")
    logout(request)
    messages.info(request, "logged out")
    return redirect("/invoice")


@login_required
def index(request):
    user = CustomUser.objects.get(id=request.user.id)
    logger.debug(request.user.is_active)
    if request.user.is_authenticated:
        messages.success(request, "logged in")
    return render(
        request,
        "invoice/index.html",
        {"user": user, "messages": messages.get_messages(request)},
    )


@login_required
def profile_user(request):

    if request.method == 'GET':
        logger.debug(request)
        user = CustomUser.objects.get(user_emp_code=request.user)
        return render(request, "partials/profile.html", {"user": user})


@login_required
def table_view(request):
    table_name = request.GET.get("table_name")
    logger.debug(table_name)
    user_id = request.user.id
    data = db.get_datarow_q(table_name, user_id)
    if not data:
        # Initialize table
        redirect("invoice:create_table")
    paginator = Paginator(data, 10)
    page_number = request.GET.get("page")
    logger.debug(page_number)
    page_obj = paginator.get_page(page_number)
    rows = [obj.get("table_data") for obj in page_obj]
    context = {"rows": rows, "page_obj": page_obj, "table_name": table_name}
    response = render(request, "partials/tableview.html", context)
    response['Cache-Control'] = 'no-cache, must-revalidate'
    return response

## USER ##


@login_required
@permission_required('invoice.view_form', raise_exception=True)
def form_view(request):
    FORMHANDLER = {
        "customer": {
            "form_class": df.customer,
            "table_name": "customer",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "customer"},
                    "hx_req": "/invoice/form_view"
                },
                "reset": {
                    "hx_vals": {"form": "customer"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "supplier": {
            "form_class": df.supplier,
            "table_name": "supplier",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "supplier"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "signatory": {
            "form_class": df.signatory,
            "table_name": "signatory",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "signatory"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "export_fields": {
            "form_class": df.export_fields,
            "table_name": "export_fields",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "export_fields"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "item_category": {
            "form_class": df.item_category,
            "table_name": "item_category",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "item_category"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "variety": {
            "form_class": df.variety,
            "table_name": "variety",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "variety"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "items": {
            "form_class": df.items,
            "table_name": "items",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "items"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "stock": {
            "form_class": df.stock,
            "table_name": "stock",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "stock"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "units": {
            "form_class": df.units,
            "table_name": "units",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "units"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "location": {
            "form_class": df.location,
            "table_name": "location",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "location"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "open_bal_prod": {
            "form_class": df.open_bal_prod,
            "table_name": "open_bal_prod",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "open_bal_prod"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "prod_record": {
            "form_class": df.prod_record,
            "table_name": "prod_record",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "prod_record"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "prod_plus_minus": {
            "form_class": df.prod_plus_minus,
            "table_name": "prod_plus_minus",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "prod_plus_minus"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "prod_approval": {
            "form_class": df.prod_approval,
            "table_name": "prod_approval",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "prod_approval"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "invoice_direct": {
            "form_class": df.invoice_direct,
            "table_name": "invoice_direct",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "invoice_direct"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "jumbo_roll_qc": {
            "form_class": df.jumbo_roll_qc,
            "table_name": "jumbo_roll_qc",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "jumbo_roll_qc"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "lot_no_wise_qc": {
            "form_class": df.lot_no_wise_qc,
            "table_name": "lot_no_wise_qc",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "lot_no_wise_qc"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "finishing_house": {
            "form_class": df.finishing_house,
            "table_name": "finishing_house",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "finishing_house"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "program_planning": {
            "form_class": df.program_planing,
            "table_name": "program_planning",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "program_planning"},
                    "hx_req": "/invoice/form_view"
                },
            }
        },
        "view_table": {
            "form_class": bf.table_view,
            "table_name": "table_view",
            "buttons": {
                "submit": {
                    "hx_vals": {"form": "table_view"},
                    "hx_req": "/invoice/form_view"
                },
            }
        }
    }
    formdata = None
    buttons = []
    hx_req = "/invoice/form_view"
    if request.method == "POST":
        formtype = request.POST.get("form")
        logger.debug(formtype)
        if formtype in FORMHANDLER:
            handler = FORMHANDLER[formtype]
            formdata = handler["form_class"](request.POST)
            for key in handler["buttons"]:
                hx_vals = handler["buttons"][key]["hx_vals"]
                hx_req = handler["buttons"][key]["hx_req"]
                button = df.button(key, hx_vals, hx_req)
                buttons.append(button)
            if formdata.is_valid():
                logger.debug("data validated")
                data = formdata.cleaned_data
                user_id = request.user.id
                logger.debug(user_id)
                if db.set_data(handler["table_name"], data, user_id):
                    logger.debug("data is saved")
                    messages.success(request, "data saved")
                else:
                    redirect("invoice:create_table")
                formdata = handler["form_class"]()
            else:
                logger.debug("data invalid")
                logger.debug(formdata.errors)
    else:
        formtype = request.GET.get("form")
        if formtype in FORMHANDLER:
            handler = FORMHANDLER[formtype]
            formdata = handler["form_class"]()
            for key in handler["buttons"]:
                hx_vals = handler["buttons"][key]["hx_vals"]
                hx_req = handler["buttons"][key]["hx_req"]
                button = df.button(key, hx_vals, hx_req)
                buttons.append(button)
    context = {
        "form": formdata,
        "buttons": buttons,
        "messages": messages.get_messages(request)
    }

    return render(request, "partials/forms.html", context)


## ADMIN ##


@login_required
def form_setup(request):

    if request.method == 'POST':
        # get the config
        logger.debug("data sent to form setup ")
        formname = "Form Name"
        username = request.POST.get("User Name")
        read = request.POST.get("Read")
        write = request.POST.get("Write")
        tablenames = request.POST.get("Tables")
        description = request.POST.get("Description")
        form_config.create_form(
            formname, username, read, write, tablenames, description
        )

        logger.debug("redirect to field config page")
        # TODO: save in cache
        return HttpResponse(df.addFieldshtml())


@login_required
def field_setup(View):
    if request.method == 'GET':
        return HttpResponse(df.fieldConfightml())

    if request.method == 'POST':
        fieldtype = request.POST.get("field type")
        label = request.POST.get("Field Name")
        disabled = request.POST.get("Disabled")
        tableRow = request.POST.get("Table Row")
        tableColumn = request.POST.get("Table Column")
        fieldno = cache.get("fieldno")
        # add_field(fieldtype, label, attr, form, fieldno, child)
        if fieldno == 0:
            cache.set("fieldno", fieldno + 1)


@login_required
def form_config(request):
    # form = df.formCreate()
    form = bf.open_bal_prod()
    return render(request, "partials/forms.html", {"form": form})


@login_required
def form_delete(request):
    form = df.formDelete()
    return render(request, "partials/forms.html", {"form": form})


@login_required
def form_edit(request):
    form = df.formEdit()
    return render(request, "partials/forms.html", {"form": form})


@login_required
def form_list(request):
    # TODO: form list
    hx_req = 'hx-post="/invoice/report_view"'
    context = {"table": data, "hx_req": hx_req, "buttons": buttons,
               "messages": messages.get_messages(request)}
    return render(request, "partials/forms.html", context)


@login_required
def table_list(request):
    # TODO: form list
    hx_req = 'hx-post="/invoice/table_view"'
    data = TableName.objects.values("table_name")
    form = df.table_view()
    hx_vals = {"": ""}
    buttons = df.buttons(hx_vals, hx_req)
    context = {"form": form, "hx_req": hx_req, "buttons": buttons,
               "messages": messages.get_messages(request)}
    return render(request, "partials/forms.html", context)


@login_required
def report_view(request):
    if request.method == "POST":
        # create report
        # tableView with list of tag and data
        pass
    else:
        # show the same report form
        pass


@login_required
def report_list(request):
    # TODO: form list
    hx_req = 'hx-post="/invoice/report_view"'
    context = {"table": data, "hx_req": hx_req, "buttons": buttons,
               "messages": messages.get_messages(request)}
    return render(request, "partials/forms.html", context)


@login_required
def create_report(request):
    if request.method == "POST":
        if request.POST.get("form") == "new_report":
            form = df.new_report(request.POST)
            buttons = df.button("new_report")
            if form.is_valid():
                logger.debug("data validated")
                # TODO: use create report
    else:
        if request.GET.get("form") == "pendingorder":
            context = {"form": formdata, "buttons": buttons,
                       "messages": messages.get_messages(request)}
    return render(request, "partials/forms.html", context)


@login_required
def edit_report(request):
    pass


@login_required
def del_report(request):
    pass


@login_required
def create_table(request):
    if request.method == "POST":
        form = bf.table_create(request.POST)
        buttons = df.button(
            "submit", {"form": "table_create"}, "/invoice/create_table")
        if form.is_valid():
            data = form.cleaned_data
            if db.new_table(data.table_name, request.user.id):
                messages.info(request, "table added")
    context = {"form": formdata, "buttons": buttons,
               "messages": messages.get_messages(request)}
    return render(request, "partials/forms.html", context)
