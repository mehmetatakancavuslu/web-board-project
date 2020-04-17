from django.urls import path
from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.home, name='home'),
    path('boards/<pk>/', views.board_topics, name='board_topics'),
    path('boards/<pk>/new/', views.new_topic, name='new_topic'),
    path('boards/<pk>/topics/<topic_pk>/', views.topic_posts, name='topic_posts'),

]
