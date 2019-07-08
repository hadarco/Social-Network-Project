from .forms import *
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile

User = get_user_model()


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.username = "testuser"
        new_user = User.objects.create(username=self.username)

    def test_profile_created(self):
        username = self.username
        user_profile = UserProfile.objects.filter(user__username=self.username)
        self.assertTrue(user_profile.exists())
        self.assertTrue(user_profile.count()== 1)
 

class TestUser(TestCase):

    def test_login(self):
        response = self.client.post("/login", {"username": "lior", "password": "12345678a"})
        print(response.status_code)
        self.assertTrue(response.status_code == 301)
        self.assertTrue(self.client.get('/login').status_code == 301)             

    def test_logout(self):
        self.client = Client()
        self.client.login(username='lior', password='12345678a')
        self.assertTrue(self.client.get('/logout/').status_code== 302)


class Form_Test(TestCase):
    def test_register_valid(self):                
        form = UserRegisterForm(data={'username': "test1", 'email': "bl2@gmail.com", 'password': "12345678a",
                                      'password2': "12345678a"})
        self.assertTrue(form.is_valid())


    def test_register_invalid_no_pass2(self):        
        form = UserRegisterForm(data={'username': "lior", 'email': "mp@gmail.com", 'password': "12345678a", 'password2': ""})
        self.assertFalse(form.is_valid())


    def test_register_invalid_no_user(self):        
        form = UserRegisterForm(data={'username': "", 'email': "mp@gmail.com", 'password': "12345678a", 'password2': "12345678a"})
        self.assertFalse(form.is_valid())


    def test_register_invalid_no_pass1(self):        
        form = UserRegisterForm(data={'username': "test1", 'email': "mp@gmail.com", 'password': "", 'password2': "12345678a"})
        self.assertFalse(form.is_valid())


    def test_register_invalid_no_email(self):        
        form = UserRegisterForm(data={'username': "test1", 'email': "", 'password': "12345678a", 'password2': "12345678a"})
        self.assertFalse(form.is_valid())



    def test_register_invalid_not_valid_email(self):        
        form = UserRegisterForm(data={'username': "test1", 'email': "m", 'password': "12345678a", 'password2': "12345678a"})
        self.assertFalse(form.is_valid())




    def test_register_invalid_not_same_pass(self):        
        form = UserRegisterForm(data={'username': "test1", 'email': "m@gmail.com", 'password': "123", 'password2': "12345678a"})
        self.assertFalse(form.is_valid())



    def test_register_invalid_pass(self):        
        form = UserRegisterForm(data={'username': "test1", 'email': "m@gmail.com", 'password': "12", 'password2': "123"})
        self.assertFalse(form.is_valid())




