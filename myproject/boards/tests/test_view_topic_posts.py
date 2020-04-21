from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Board, Post, Topic
from ..views import PostListView

class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', description='Django board')
        user = User.objects.create_user('john', 'john@doe.com', '123')
        topic = Topic.objects.create(subject='Hello, world', board=board,
                                     starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet',
                            topic=topic, created_by=user)
        self.url = reverse('boards:topic_posts', kwargs={'pk': board.pk,
                                             'topic_pk': topic.pk})
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, PostListView)
