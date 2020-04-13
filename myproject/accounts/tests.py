from django.test import TestCase
from django.urls import resolve, reverse
from .views import signup

# Create your tests here.
class SignUpTests(TestCase):
    def test_signup_status_code(self):
        """
        Request to signup url returns a response with a status code of 200.
        """
        url = reverse('accounts:signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup_url_resolves_signup_vies(self):
        """
        Signup url resolves to the signup view.
        """
        view = resolve('/signup/')
        self.assertEqual(view.func, signup)
