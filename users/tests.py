from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data = {
                "username" : "Sirojiddin",
                "first_name" : "Sirojiddin",
                "last_name" : "Samadov",
                "email" : "siroj@gmail.com",
                "password" : "joris94@07",

            }
        )

        user = User.objects.get(username="Sirojiddin")

        self.assertEqual(user.first_name, 'Sirojiddin')
        self.assertEqual(user.last_name, 'Samadov')
        self.assertEqual(user.email, 'siroj@gmail.com')
        self.assertNotEqual(user.password, 'joris94@07')
        self.assertTrue(user.check_password("joris94@07"))

    def test_required_fields(self):
        response = self.client.post(
           reverse("users:register"),
            data = {
                "first_name" : "Sirojiddin",
                "email" : "siroj@gmail.com"
            }
        )
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Sirojiddin",
                "first_name": "Sirojiddin",
                "last_name": "Samadov",
                "email": "invalid-email",
                "password": "joris94@07", } )
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        # 1. create a user
        user = User.objects.create(username='Sirojiddin', first_name='Sirojiddin')
        user.set_password("somepassword")
        user.save()

        # 2. try to create another user with the same username
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Sirojiddin",
                "first_name": "Sirojiddin",
                "last_name": "Samadov",
                "email": "siroj@gmail.com",
                "password": "joris94@07", } )

        # 3. check that the second user was not created
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

        # 4. check that the form contains the error message
        self.assertFormError(response, "form", "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        # DRY - Don't repeat yourself
        self.user = User.objects.create(username='Sirojiddin', first_name='Sirojiddin')
        self.user.set_password('somepass')
        self.user.save()

    def test_succesful_login(self):
        self.client.post(
            reverse("users:login"),
            data = {
                'username' : 'Sirojiddin',
                'password' : 'somepass'
            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data = {
                'username': 'wrong-username',
                'password': 'somepass'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data = {
                'username': 'Sirojiddin',
                'password': 'wrong-password'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        # login user
        self.client.login(username='Sirojiddin', password='somepass')

        # send request to logout
        self.client.get(reverse("users:logout"))

        # take that user and check he is login
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)  # if false, logout is working


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")


    def test_profile_details(self):
        user = User.objects.create(
            username = "Sirojiddin",
            first_name = "Sirojiddin",
            last_name = "Samadov",
            email = "siroj@gmail.com"
        )
        user.set_password("somepass")
        user.save()

# shu userni login qilish kk, uning uchun "login" metodidan foydalan

        self.client.login(username = "Sirojiddin", password = "somepass")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)







