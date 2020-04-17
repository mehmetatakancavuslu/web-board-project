from django.test import TestCase
from django.urls import reverse, resolve
from ..views import home
from ..models import Board

# Create your tests here.
class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django',
                                          description='Django board.')
        url = reverse('boards:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        """
        Request to home url returns a response with a status code of 200.
        """
        self.assertEqual(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """
        Home url resolves to the home view.
        """
        view = resolve('/')
        self.assertEqual(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        """
        Check that home url response contains the link to the board created.
        """
        board_topics_url = reverse('boards:board_topics', args=[self.board.pk])
        self.assertContains(self.response,
                            'href="{0}"'.format(board_topics_url))
