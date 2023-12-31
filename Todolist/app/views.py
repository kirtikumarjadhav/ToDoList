from typing import Any
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.views.generic.edit import CreateView, UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone

# Create your views here.


def Homepage(request):
    return render(request,'homepage.html')    


class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('TaskList')

class RegisterPage(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('TaskList')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('TaskList')
        return super(RegisterPage,self).get(*args,**kwargs)


class TaskList(LoginRequiredMixin,ListView):
    model = Task 
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user=self.request.user)
        context['count']= context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
        
        context['search_input'] = search_input

        context['current_day'] = timezone.now().strftime('%A') 
        context['current_time'] = timezone.now().strftime('%H:%M:%S')

        tasks_with_due_dates = []
        for task in context['tasks']:
            task.due_date_str = task.due_date.strftime('%Y-%m-%d %H:%M:%S') if task.due_date else 'No due date'
            tasks_with_due_dates.append(task)
        context['tasks_with_due_dates'] = tasks_with_due_dates
        
        return context




class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'app/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('TaskList')


    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('TaskList')

class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    
    success_url = reverse_lazy('TaskList')    


def Features(request):
    return render(request,'features.html')

def ForTeams(request):
    return render(request,'forteams.html')



