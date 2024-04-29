from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User

from django.http import JsonResponse
from .serializers import UserSerializer

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

# API creation Code 
@csrf_exempt
def AllUserData(request):
    try:
        all_users_data = User.objects.all()
    except:
        data = {
            "message":"Not Found, Sorry!",
            "status": 404
        }
        return JsonResponse(data)

    if request.method == "GET":
        users_data =  UserSerializer(all_users_data, many = True)
        return JsonResponse(users_data.data, safe = False)
    
    elif request.method == "POST":
        input_data = JSONParser().parse(request)
        de_serializer = UserSerializer(data = input_data)

        if de_serializer.is_valid():
            de_serializer.save()
            return JsonResponse(de_serializer.data, status = 201)
        else:
            return JsonResponse(de_serializer.errors, status = 400)

@csrf_exempt
def SingleUserData(request, id):
    try:
        user_data = User.objects.get(pk=id)
    except:
        data = {
            "message":"Not Found, Sorry!",
            "status": 404
        }
        return JsonResponse(data)
    
    if request.method == 'GET':
        single_user = UserSerializer(user_data)
        return JsonResponse(single_user.data, status = 200)
    
    elif request.method == 'PUT':

        input_data = JSONParser().parse(request)
        de_serializer = UserSerializer(user_data,input_data)

        if de_serializer.is_valid():
            de_serializer.save()
            return JsonResponse(de_serializer.data, status = 205)
        else:
            return JsonResponse(de_serializer.errors, status = 400)

    
    elif request.method == "DELETE":
        user_data.delete()
        data = {
            "message":"Successfully Delete",
            "status": 204
        }
        return JsonResponse(data)