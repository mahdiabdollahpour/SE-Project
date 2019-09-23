from django import forms
from django.forms import ValidationError
from django.conf import settings
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from phonenumber_field.formfields import PhoneNumberField


class CreateTeamForm(forms.Form):
    class Meta:
        pass

    def clean_team_name(self):
        pass

    def clean_admin_name(self):
        pass


class CreateProjectForm(forms.Form):
    class Meta:
        pass

    def clean_project_name(self):
        pass


class CreateTaskForm(forms.Form):
    class Meta:
        pass

    def clean_task_name(self):
        pass


class TaskMemberAdditionForm(forms.Form):
    class Meta:
        pass

    def clean_task_id(self):
        pass

    def clean_user(self):
        pass


class EditTaskStatusForm(forms.Form):
    class Meta:
        pass

    def clean_task_id(self):
        pass

    def clean_user(self):
        pass

    def clean_status(self):
        pass


class UploadTaskResultForm(forms.Form):
    class Meta:
        pass

    def clean_task_id(self):
        pass

    def clean_user(self):
        pass

    def clean_result(self):
        pass


class EditTeamSettingsForm(forms.Form):
    class Meta:
        pass

    def clean_name(self):
        pass

    def clean_description(self):
        pass

    def clean_image(self):
        pass


class EditProjectSettingsForm(forms.Form):
    class Meta:
        pass

    def clean_name(self):
        pass

    def clean_description(self):
        pass

    def clean_image(self):
        pass


class EditTaskSettingsForm(forms.Form):
    class Meta:
        pass

    def clean_name(self):
        pass

    def clean_description(self):
        pass

    def clean_image(self):
        pass

    def clean_deadline(self):
        pass
