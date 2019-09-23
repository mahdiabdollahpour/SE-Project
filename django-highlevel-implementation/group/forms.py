from django import forms
from django.forms import ValidationError
from django.conf import settings
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from phonenumber_field.formfields import PhoneNumberField


class CreateGroupForm(forms.Form):
    class Meta:
        pass

    def clean_group_name(self):
        pass

    def clean_admin_name(self):
        pass


class EditGroupSettingsForm(forms.Form):
    class Meta:
        pass

    def clean_name(self):
        pass

    def clean_description(self):
        pass

    def clean_image(self):
        pass

    def clean_link_visibility(self):
        pass

