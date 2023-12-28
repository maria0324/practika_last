from datetime import datetime

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from .forms import UserRegisterForm
from .models import Request
from django.contrib.auth.decorators import login_required
from .forms import CreateRequestForm
from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


class BBLoginView(LoginView):
    template_name = 'main/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class RegistrateUser(CreateView):
    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        form = {'form': RegistrateUser()}
        return render(request, 'main/registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, 'main/register_done.html', {'form': form})
        return render(request, 'main/registration.html', {'form': form})


class CreateRequest(CreateView):
    model = Request
    template_name = 'main/create_request.html'
    success_url = reverse_lazy('index')
    form_class = CreateRequestForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DeleteRequest(DeleteView):
    model = Request
    template_name = 'main/delete_request.html'
    success_url = reverse_lazy('index')

class DeleteRequestFilter(DeleteView):
    model = Request
    template_name = 'main/delete_request.html'
    success_url = reverse_lazy('index')

class ViewProcessRequests(ListView):
    model = Request
    template_name = 'main/index.html'
    context_object_name = 'requests'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_of_accepted_requests"] = Request.objects.filter(status__exact='Принято в работу').count
        return context

class ViewRequests(ListView):
    model = Request
    template_name = 'main/profile.html'
    context_object_name = 'requests'
    def get_queryset(self):
       return Request.objects.filter(author=self.request.user)

@login_required
def profile(request):
    return render(request, 'main/profile.html')

class RequestListView(ListView):
    model = Request
    template_name = 'main/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        status = self.request.GET.get('status')
        if status:
            return Request.objects.sort(status=status)
        return Request.objects.all()


