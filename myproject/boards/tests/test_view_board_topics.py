from django.test import TestCase
from django.urls import reverse, resolve
from ..views import TopicListView
from ..models import Board

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
        self.assertEqual(view.func.view_class, TopicListView)

    def test_board_topics_view_contains_navigation_links(self):
        """
        Board_topics page contains links to home and new_topic pages.
        """
        board_topics_url = reverse('boards:board_topics', args=[1])
        homepage_url = reverse('boards:home')
        new_topic_url = reverse('boards:new_topic', args=[1])
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
