from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=500)
    slug = models.SlugField()
    image = models.URLField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    ans = models.PositiveSmallIntegerField(
        choices=((1, 1), (2, 2), (3, 3), (4, 4)))

    def __str__(self):
        return self.question


class Scores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(null=True, blank=True)
