from django.test import TestCase
from django.urls import resolve, reverse
from ..views import signup
from ..forms import SignUpForm
from django.contrib.auth.models import User

# Create your tests here.
class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        """
        Request to signup url returns a response with a status code of 200.
        """
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_signup_vies(self):
        """
        Signup url resolves to the signup view.
        """
        view = resolve('/signup/')
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        """
        Signup view contains csrf token.
        """
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """
        Signup view contains SignUpForm.
        """
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        """
        The view must contain five inputs: csrf, username, email, password1,
        password2
        """
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SuccesfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('boards:home')

    def test_redirection(self):
        """
        A valid form submission redirects the user to the home page.
        """
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        """
        User object is succesfully created.
        """
        self.assertTrue(User.objects.exists)

    def test_user_authentication(self):
        """
        The resulting reponse from a new request to an arbitrary page,
        should have a 'user' in its context after a succesful signup.
        """
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        """.
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        """
        Response context of an invalid form submission should have errors.
        """
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        """
        No User object is created.
        """
        self.assertFalse(User.objects.exists())
