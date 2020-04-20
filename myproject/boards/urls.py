from django.urls import path
from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('boards/<pk>/', views.board_topics, name='board_topics'),
    path('boards/<pk>/new/', views.new_topic, name='new_topic'),
    path(
        'boards/<pk>/topics/<topic_pk>/',
        views.topic_posts,
        name='topic_posts'
    ),
    path(
        'boards/<pk>/topics/<topic_pk>/reply/',
        views.reply_topic,
        name='reply_topic'
    ),
    path('boards/<pk>/topics/<topic_pk>/posts/<post_pk>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'
    )
]
