from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
import logging
from ..cachestore import cachestore as cache
from ..models import *
from ..form_files import *
from ..form_files import Base as bf

# IMPROVEMENT NEEDED: Add proper docstring for the module
# IMPROVEMENT NEEDED: Add proper type hints for better code maintainability
# IMPROVEMENT NEEDED: Consider splitting views into separate files (auth_views.py, form_views.py, etc.)

logger = logging.getLogger(__name__)


# IMPROVEMENT NEEDED: Add rate limiting for login attempts
# IMPROVEMENT NEEDED: Add proper error handling and logging
# IMPROVEMENT NEEDED: Add proper session management

@ensure_csrf_cookie
@csrf_protect
def login_user(request):
    if request.method == 'POST':
        form = bf.loginForm(request.POST, request=request)
        if form.is_valid():
            login(request, form.user)
            return redirect('invoice:index')
    else:
        form = bf.loginForm(request=request)

    response = render(request, "invoice/login.html", {
        "login": form,
        "messages": messages.get_messages(request)
    })
    response['HX-Trigger-After-Swap'] = "showNotif"
    return response

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging
# IMPROVEMENT NEEDED: Add proper form validation messages


@ensure_csrf_cookie
@csrf_protect
@login_required
def change_password(request):
    if not isinstance(request.user, CustomUser):
        messages.error(request, 'Invalid user session.')
        return redirect('invoice:login')

    if request.method == 'POST':
        form = bf.changePassword(request.POST)
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
                    form.add_error('new_password', str(e))
                else:
                    # Set the new password
                    request.user.set_password(new_password)
                    request.user.save()
                    # Keep user logged in
                    update_session_auth_hash(request, request.user)
                    messages.success(
                        request, 'Your password was changed successfully.')
                    return redirect('invoice:index')
    else:
        form = bf.changePassword()

    return render(request, 'invoice/passwordChange.html', {
        'form': form,
        'messages': messages.get_messages(request)
    })

# IMPROVEMENT NEEDED: Add proper session cleanup
# IMPROVEMENT NEEDED: Add proper logging


@ensure_csrf_cookie
@csrf_protect
@login_required
def logout_user(request):
    logger.debug("logout")
    logout(request)
    messages.info(request, "logged out")
    response = redirect("/invoice")
    response['HX-Trigger-After-Swap'] = 'showNotif'
    return response


# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging
# IMPROVEMENT NEEDED: Add proper user feedback
