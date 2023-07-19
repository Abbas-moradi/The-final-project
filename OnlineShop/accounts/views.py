from django.shortcuts import render
from django.views import View
from .forms import UserRegisterationForm


class UserRegisterView(View):
    form_class = UserRegisterationForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form': form})

    def post(self):
        pass

