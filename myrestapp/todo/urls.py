from django.urls import path, include

from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index_view),
    path('api/todo/', views.ToDoItemView.as_view()),
    path('api/todo/<int:pk>', views.ToDoDetailView.as_view()),
]