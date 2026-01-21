from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DeleteView, ListView)
from django.urls import (reverse_lazy, reverse)
from django_htmx.http import trigger_client_event
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from ..form_files import (helperFunct as hf, millsoftForm as mf)
from ..models import (RChallan)
import logging
logger = logging.getLogger(__name__)


class RChallan_
