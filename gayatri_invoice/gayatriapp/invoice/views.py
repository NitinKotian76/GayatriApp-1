from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse_lazy
from django.views import View
import logging
from .cachestore import cachestore as cache
from .models import *
from .forms import *
from .formmod import DefaultForm as df
from .formmod import BaseForm as bf
from .dbmod import dbfunctions as db
from .reportmod import create_report as cr
from . import mappings as mp
from django.core.paginator import Paginator
from django.contrib import messages


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
def change_password(request):
    if request.method == 'POST':
        FORMHANDLER = mp.COMMON
        buttons = []
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check old password is correct
            if not check_password(old_password, request.user.password):
                form.add_error('old_password', 'Old password is incorrect.')
                # Check new passwords match
            elif new_password != confirm_password:
                form.add_error('confirm_password',
                               'New passwords do not match.')
            else:
                # Validate the new password with Django's validators
                try:
                    validate_password(new_password, user=request.user)
                except Exception as e:
                    form.add_error('new password invalid', e)
                else:
                    # Set the new passwords
                    request.user.set_password(new_password)
                    request.user.save()
                    # Keeps user logged in
                    update_session_auth_hash(request, request.user)
                    messages.success(
                        request, 'Your password was changed successfully.')
                    return redirect(reverse_lazy('index'))
    else:
        form = ChangePasswordForm()
        for key in handler["buttons"]:
            hx_vals = handler["buttons"][key]["hx_vals"]
            hx_req = handler["buttons"][key]["hx_req"]
            button = df.button(key, hx_vals, hx_req)
            buttons.append(button)
    context = {'form': form, "buttons": buttons}
    return render(request, 'change_password.html', context)


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
    FORMHANDLER = mp.FORMHANDLER
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
