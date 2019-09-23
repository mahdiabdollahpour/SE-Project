from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView,
)
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView, DetailView, ListView, RedirectView, UpdateView
from django.conf import settings

# from .utils import (
#     send_activation_email, send_forgotten_username_email, send_activation_change_email,
# )
from .forms import *
from .models import *


# Create your views here.


class CreateGroupView(LoginRequiredMixin, FormView):
    template_name = _
    form_class = CreateGroupForm

    def form_valid(self, form):
        pass


class GroupView(LoginRequiredMixin, DetailView):
    model = _
    template_name = _


class GroupMembersView(LoginRequiredMixin, DetailView):
    model = _
    template_name = _


class EditGroupSettingsView(LoginRequiredMixin, UpdateView):
    template_name = _
    form_class = EditGroupSettingsForm

    def form_valid(self, form):
        pass
