from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
from halls.forms import VideoForm, SearchForm
from halls.models import Hall, Video


def index(request):
    return render(request, "pages/index.html")


def dashboard(request):
    return render(request, "pages/dashboard.html")


def addVideo(request, pk):
    form = VideoForm
    search = SearchForm
    hall = Hall.objects.get(pk=pk)
    if request.method == "POST":
        filled_form = VideoForm(request.POST)
        if filled_form.is_valid():
            video = Video()
            video.title = filled_form.cleaned_data['title']
            video.url = filled_form.cleaned_data['url']
            video.youtube_id = filled_form.cleaned_data['youtube_id']
            video.hall = Hall.objects.get(pk=pk)
            video.save()
            return redirect(request.path)
    return render(request, "halls/addVideo.html", {'form':form, 'search': search, 'hall': hall})


def videoSearch(request):
    return JsonResponse({'data':"dasda"})


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
