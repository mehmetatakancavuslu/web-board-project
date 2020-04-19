from django.test import TestCase
from ..models import Board, Topic, Post
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.urls import reverse

class ModelsTestCase(TestCase):
    """
    Base test case to be used in all model tests
    """
    def setUp(self):
        self.board = Board.objects.create(name='Django',
                                          description='Django board.')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username,
                                        email='john@doe.com',
                                        password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world',
                                          board=self.board, starter=user)
        self.message = 'Lorem ipsum dolor sit amet, consectetur adipiscing. '
        self.message += 'Nulla nec velit eu mauris viverra sollicitudin. '
        self.message += 'Donec convallis tincidunt tincidunt. Proin et, '
        self.message += 'tincidunt magna. Cras vel bibendum neque. Curabitur '
        self.message += 'nibh ac venenatis. Ut vel metus eu lacus finibus. '
        self.message += 'Sed ut ultricies diam. Sed consequat finibus justo. '
        self.message += 'Etiam eu consectetur turpis, vel tempus lorem. In '
        self.message += 'tincidunt.'
        self.post = Post.objects.create(message=self.message,
                                        topic=self.topic, created_by=user)
        self.url = reverse('boards:reply_topic',
                           kwargs={'pk': self.board.pk,
                                   'topic_pk': self.topic.pk})

class BoardModelTests(ModelsTestCase):
    def test_string_representation(self):
        self.assertEqual(str(self.board), 'Django')

class TopicModelTests(ModelsTestCase):
    def test_string_representation(self):
        self.assertEqual(str(self.topic), 'Hello, world')

class PostModelTests(ModelsTestCase):
    def test_string_representation(self):
        truncated_message = Truncator(self.post.message)
        self.assertEqual(str(self.post), truncated_message.chars(30))
