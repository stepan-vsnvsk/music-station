from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings
from django.contrib import admin
from django.urls import reverse


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(blank=True)
    modified = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?')

    def __str__(self):
        return '<Question: {}>'.format(self.question_text)

    def save(self, *args, **kwargs):
        # update modified
        if not self.id:
            self.pub_date = timezone.now()
        else:
            self.modified = True
            self.pub_date = timezone.now()
        return super(Question, self).save(*args, **kwargs)    
    
    def has_recently_added_posts(self):
        one_day_before = timezone.now() - datetime.timedelta(days=2)
        return self.post_set.filter(timestamp__gte = one_day_before)

    def get_absolute_url(self):
        return reverse('posts:discussion', args=[str(self.id)])


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return '<Choice {}>'.format(self.choice_text)


class Post(models.Model):
    body = models.TextField(max_length=450)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return '<Post: {}>'.format(self.body)

    def save(self, *args, **kwargs):
        # timestamp for modified posts
        if not self.id:
            self.timestamp = timezone.now()
        else:
            self.modified = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):        
        return reverse('posts:discussion', args=[str(self.question.id)])