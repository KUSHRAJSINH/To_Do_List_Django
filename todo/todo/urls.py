from django.contrib import admin
from django.urls import path
from todo_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('task_list/', views.task_list, name='task_list'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('register/', views.register_user, name='register'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
