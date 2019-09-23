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
from .forms import (
    SignInViaUsernameForm, SignUpForm,
    RemindUsernameForm,
    ChangeProfileForm,
    AddContactForm,
    EditContactsForm,
    BlockUserForm
)
from .models import User, Activation

from django.urls import reverse


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated4
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LogInView(GuestOnlyView, FormView):
    template_name = 'accounts/log_in.html'

    @staticmethod
    def get_form_class(**kwargs):
        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    # The default implementation for form_valid() simply redirects to the success_url.
    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                # If value is 0, the user’s session cookie will expire when the user’s Web browser is closed.
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)

        return redirect(settings.LOGIN_REDIRECT_URL)


class SignUpView(GuestOnlyView, FormView):
    template_name = 'accounts/sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)

        if settings.DISABLE_USERNAME:
            # Set a temporary username
            user.username = get_random_string()
        else:
            user.username = form.cleaned_data['username']

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        # Create a user record
        user.save()

        # Change the username to the "user_ID" form
        # if settings.DISABLE_USERNAME:
        #     user.username = f'user_{user.id}'
        #     user.save()

        if settings.ENABLE_USER_ACTIVATION:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = form.cleaned_data['email']
            act.save()

            send_activation_email(request, user.email, code)

            messages.success(
                request, _('You are signed up. To activate the account, follow the link sent to the mail.'))
        else:
            raw_password = form.cleaned_data['password1']

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            messages.success(request, _('You are successfully signed up!'))

        return redirect(settings.HOME)


class ActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Activate profile
        user = act.user
        user.is_active = True
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully activated your account!'))

        return redirect('accounts:log_in')


class EditProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/change_profile.html'
    form_class = ChangeProfileForm

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['name'] = user.name
        initial['image'] = user.image
        initial['bio'] = user.bio
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.name = form.cleaned_data['name']
        user.image = form.cleaned_data['image']
        user.bio = form.cleaned_data['bio']
        user.save()

        messages.success(self.request, _('Profile data has been successfully updated.'))

        return redirect(settings.LOGIN_REDIRECT_URL)


class RemindUsernameView(GuestOnlyView, FormView):
    template_name = 'accounts/remind_username.html'
    form_class = RemindUsernameForm

    # def form_valid(self, form):
    #     user = form.user_cache
    #     send_forgotten_username_email(user.email, user.username)
    #
    #     messages.success(self.request, _('Your username has been successfully sent to your phone.'))
    #
    #     return redirect('accounts:remind_username')


class RestorePasswordView(GuestOnlyView, FormView):
    # template_name = 'accounts/restore_password.html'
    #
    # @staticmethod
    # def get_form_class(**kwargs):
    #     return RestorePasswordForm
    #
    # def form_valid(self, form):
    #     user = form.user_cache
    #     token = default_token_generator.make_token(user)
    #     uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
    #     send_reset_password_email(self.request, user.email, token, uid)
    #
    #     return redirect('accounts:restore_password_done')
    pass


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'accounts/log_out.html'


# bara moshahede profile
class UserDetailView(LoginRequiredMixin, DetailView):
    # model = User
    # template_name = 'accounts/user_detail.html'
    # slug_field = 'username'
    # slug_url_kwarg = 'username'
    pass


#
# class UserRedirectView(LoginRequiredMixin, RedirectView):
#
#     def get_redirect_url(self):
#         return reverse('accounts:detail',
#                        kwargs={'username': self.request.user.username})


# class UserUpdateView(LoginRequiredMixin, UpdateView):
#     fields = ['name', 'image', 'bio', ]
#     model = User
#     template_name = 'accounts/user_form.html'
#
#     def get_success_url(self):
#         return reverse('accounts:detail',
#                        kwargs={'username': self.request.user.username})
#
#     def get_object(self, **kwargs):
#         # Only get the User record for the user making the request
#         return User.objects.get(username=self.request.user.username)

class AddContactView(LoginRequiredMixin, FormView):
    template_name = _
    form_class = AddContactForm

    def form_valid(self, form): pass


class EditContactView(LoginRequiredMixin, UpdateView):
    template_name = _
    form_class = EditContactsForm

    def form_valid(self, form): pass


class ContactListView(LoginRequiredMixin, ListView):
    model = _
    template_name = _
    pass


class BlockUserView(LoginRequiredMixin, FormView):
    template_name = _
    form_class = BlockUserForm

    def form_valid(self, form): pass
