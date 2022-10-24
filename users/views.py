from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

# NOTE: TODO make AlreadyAuthorizedMixin and LoginRequiredMixin

from rest_framework import status

from .forms import UserLogInForm


class LogInView(TemplateView):
    """
        The view for login page
    """
    template_name = "users/login.html"
    form = UserLogInForm

    def get(self, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            login(self.request, form.user)
            #  TODO: This is a Temporary redirection
            return HttpResponseRedirect(reverse('healthcare:dashboard'))
        context = {'form': form}
        return render(self.request, self.template_name, context,
                      status=status.HTTP_400_BAD_REQUEST)

# NOTE: TODO change password view