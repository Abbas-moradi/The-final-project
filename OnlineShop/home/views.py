from django.shortcuts import render, redirect
from django.views import View


class Home(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass

