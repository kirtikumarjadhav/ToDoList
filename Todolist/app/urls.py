from django.contrib import admin
from django.urls import path
from . import views
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView,CustomLoginView,RegisterPage
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('',views.Homepage,name='Homepage'),
    path('Features/',views.Features,name='Features'),
    path('ForTeams/',views.ForTeams,name='ForTeams'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',RegisterPage.as_view(), name='register'),
    path('TaskList/',TaskList.as_view(),name='TaskList'),
    path('task/<int:pk>',TaskDetail.as_view(),name='task'),
    path('task-create/',TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>',TaskUpdate.as_view(),name='task-update'),
    path('task-detele/<int:pk>',DeleteView.as_view(),name='task-delete'),
    
    
]