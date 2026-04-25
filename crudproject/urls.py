from django.contrib import admin
from django.urls import path
from tasks import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('signup/', views.create_user, name='sign-up'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed_list, name='tasks_completed'), # NOQA
    path('task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task_completed/<int:task_id>/', views.task_completed, name='task_completed'), # NOQA
    path('task/<int:task_id>/delete', views.task_delete, name='delete'), # NOQA
    path('logout/', views.log_out, name='log-out'),
    path('login/', views.log_in, name='log-in')
]
