from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm

from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # adjust import as needed

class RegisterView(View):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    form_class = CustomUserCreationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("accounts:login")
        return render(request, self.template_name, {'form': form})
