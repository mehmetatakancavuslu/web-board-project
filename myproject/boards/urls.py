from django.urls import path
from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.board_topics, name='board_topics'),
]