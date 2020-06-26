from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
from halls.models import Hall


def index(request):
    return render(request, "pages/index.html")


def dashboard(request):
    return render(request, "pages/dashboard.html")


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = "registration/signup.html"

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get("username"), form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateHall(generic.CreateView):
    model = Hall
    fields = ["title"]
    template_name = "halls/createHall.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHall, self).form_valid(form)
        return redirect("index")


class DetailHall(generic.DetailView):
    model = Hall
    template_name = "halls/detailHall.html"


class UpdateHall(generic.UpdateView):
    model = Hall
    fields = ["title"]
    template_name = "halls/updateHall.html"
    success_url = reverse_lazy("dashboard")


class DeleteHall(generic.DeleteView):
    model = Hall
    template_name = "halls/deleteHall.html"
    success_url = reverse_lazy("dashboard")