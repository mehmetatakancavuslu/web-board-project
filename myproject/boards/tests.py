from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topics
from .models import Board

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

class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        """
        Request to a board_topics url that refers to an already existing board
        object returns a response with a status code of 200
        """
        url = reverse('boards:board_topics', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        """
        Request to a board_topics url that refers to a non-existent board
        object returns a response with a status code of 404
        """
        url = reverse('boards:board_topics', args=[99])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        """
        Board_topics url resolves to the board_topics view.
        """
        view = resolve('/boards/1/')
        self.assertEqual(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        """
        Board_topics page contains a link to home url.
        """
        board_topics_url = reverse('boards:board_topics', args=[1])
        response = self.client.get(board_topics_url)
        homepage_url = reverse('boards:home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
