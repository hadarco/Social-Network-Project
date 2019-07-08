import re

from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.
from hashtags.signals import parsed_hashtags
from .validators import validate_bad_content, validate_blank_content


# model manager

class TweetManager(models.Manager):
    def retweet(self, user, parent_obj):
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj
        
        qs = self.get_queryset().filter(
                user=user, parent=og_parent
                ).filter(
                    timestamp__year=timezone.now().year,
                    timestamp__month=timezone.now().month,
                    timestamp__day=timezone.now().day,
                    reply=False,
                )
        if qs.exists():
            return None

        obj = self.model(
                parent = og_parent,
                user = user,
                content = parent_obj.content,
            )
        obj.save()

        return obj

    def like_toggle(self, user, tweet_obj):
        if user in tweet_obj.liked.all():
            is_liked = False
            tweet_obj.liked.remove(user)
        else:
            is_liked = True
            tweet_obj.liked.add(user)
        return is_liked



class Tweet(models.Model):
    parent      = models.ForeignKey("self", blank=True, null=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL)
    content     = models.CharField(max_length=40, validators=[validate_bad_content, validate_blank_content])
    liked       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    reply       = models.BooleanField(verbose_name='reply?', default=False)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    objects = TweetManager()

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse("tweet:detail", kwargs={"pk":self.pk})

    class Meta:
        ordering = ['timestamp']

    def get_parent(self):
        return self.parent if self.parent else self

    def get_children(self):
        parent = self.get_parent()
        return Tweet.objects.filter(parent=parent) | Tweet.objects.filter(pk=parent.pk)


def tweet_save_receiver(sender, instance, created, *args, **kwargs):
    if created and not instance.parent:
        re.findall(r'@(?P<username>[\w.@+-]+)', instance.content)
        # send notification to user here.
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=re.findall(r'#(?P<hashtag>[\w\d-]+)',
                                                                                instance.content))
        # send hashtag signal to user here.


post_save.connect(tweet_save_receiver, sender=Tweet)







