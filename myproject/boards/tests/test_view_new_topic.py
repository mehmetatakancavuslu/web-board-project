from django.test import TestCase
from django.urls import reverse, resolve
from ..views import new_topic
from ..models import Board, Topic, Post
from ..forms import NewTopicForm
from django.contrib.auth.models import User

class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='John', email='john@doe.com',
                                 password='123')
        self.client.login(username='John', password='123')

    def test_new_topic_view_success_status_code(self):
        """
        Request to a new_topic url with a pk of already existing board
        object returns a response with a status code of 200
        """
        url = reverse('boards:new_topic', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        """
        Request to a new_topic url with a pk of non-existing board
        object returns a response with a status code of 404
        """
        url = reverse('boards:new_topic', args=[99])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        """
        New_topic url resolves to the new_topic view.
        """
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        """
        New_topic view contains a link to board_topics url.
        """
        new_topic_url = reverse('boards:new_topic', args=[1])
        board_topics_url = reverse('boards:board_topics', args=[1])
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        """
        New_topic view contains csrf token embedded.
        """
        url = reverse('boards:new_topic', args=[1])
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        """
        New_topic url with valid post data creates Topic and Post objects.
        """
        url = reverse('boards:new_topic', args=[1])
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists)
        self.assertTrue(Post.objects.exists)

    def test_new_topic_invalid_post_data(self):
        """
        New_topic url with invalid post data should not redirect. It shows
        the form again with validation errors.
        """
        url = reverse('boards:new_topic', args=[1])
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        """
        New_topic url post with empty fields should not redirect. It shows
        the form again with validation errors.
        """
        url = reverse('boards:new_topic', args=[1])
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        """
        New_topic view contains NewTopicForm.
        """
        url = reverse('boards:new_topic', args=[1])
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        self.url = reverse('boards:new_topic', args=[1])
        self.response = self.client.get(self.url)

    def test_redirection(self):
        """
        Non-authenticated user request to new_topic redirects to login.
        """
        login_url = reverse('accounts:login')
        redirect_url = '{login_url}?next={url}'.format(login_url=login_url,
                                                       url=self.url)
        self.assertRedirects(self.response, redirect_url)
