
from django.contrib.auth import logout
from django.views.generic import View
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

# NOTE: TODO create LoginRequiredMixin

class LogoutView(View):
    """
        The logout class
    """
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('users:login'))