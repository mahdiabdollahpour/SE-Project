from django import forms
from django.forms import ValidationError
from django.conf import settings
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from phonenumber_field.formfields import PhoneNumberField


class UserCacheMixin:
    user_cache = None


class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label=_('Remember me'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('You entered an invalid password.'))

        return password


class SignInViaUsernameForm(SignIn):
    username = forms.CharField(label=_('Username'))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['username', 'password', 'remember_me']
        return ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError(_('You entered an invalid username.'))

        # if not user.is_active:
        #     raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return username


class SignUpForm(UserCreationForm):
    agree_to_terms = forms.BooleanField(label=_('I agree to terms of service.'), required=True)
    phone = PhoneNumberField(label=_('phone'))

    class Meta:
        model = User
        fields = ['username', 'phone', 'password1', 'password2', 'agree_to_terms']

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        user = User.objects.filter(phone__iexact=phone).exists()
        if user:
            raise ValidationError(_('You can not use this phone number.'))

        return phone

    def clean_agree_to_terms(self):
        is_checked = self.cleaned_data['agree_to_terms']
        if not is_checked:
            raise ValidationError(_('Please accept terms of service.'))
        return is_checked


class RestorePasswordForm(UserCacheMixin, forms.Form):
    phone = PhoneNumberField(label=_('phone'))

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        user = User.objects.filter(phone__iexact=phone).first()
        if not user:
            raise ValidationError(_('You entered an invalid phone number.'))

        self.user_cache = user

        return phone


class ChangeProfileForm(UserCacheMixin, ModelForm):
    class Meta:
        model = User
        fields = ['name', 'image', 'bio']


class RemindUsernameForm(UserCacheMixin, forms.Form):
    phone = PhoneNumberField(label=_('phone'))

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        user = User.objects.filter(phone__iexact=phone).first()
        if not user:
            raise ValidationError(_('You entered an invalid phone number.'))

        self.user_cache = user

        return phone


class AddContactForm(UserCacheMixin, ModelForm):
    def clean_phone_number(self):
        pass


class EditContactsForm(UserCacheMixin, ModelForm):
    def clean_username(self):
        pass

    def clean_phone_number(self):
        pass


class BlockUserForm(UserCacheMixin, ModelForm):
    def clean_phone_number(self):
        pass
