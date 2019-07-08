from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

# Create your tests here.


from .models import Tweet


User = get_user_model()

class TweetModelTestCase(TestCase):
    def setUp(self):
         User.objects.create(username='tester')

    def test_tweet_item(self):
        obj = Tweet.objects.create(
                user= User.objects.first(),
                content='test'
            )
        self.assertTrue(obj.content == "test")
        self.assertTrue(obj.id == 1)

    def test_tweet_item2(self):
        obj = Tweet.objects.create(
                user= User.objects.first(),
                content='test'
            )
        self.assertTrue(obj.content == "test")
        self.assertTrue(obj.id == 1)
        absolute_url = reverse("tweet:detail", kwargs={"pk": 1})
        self.assertTrue(obj.get_absolute_url() == absolute_url)




    def test_tweet_url(self):
        obj = Tweet.objects.create(
                user= User.objects.first(),
                content='test'
            )
        absolute_url = reverse("tweet:detail", kwargs={"pk": obj.pk})
        self.assertTrue(obj.get_absolute_url() == absolute_url)
