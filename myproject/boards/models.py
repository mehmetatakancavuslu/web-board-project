from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    """
    Stores boards created by admin users.
    """
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Topic(models.Model):
    """
    Stores a single topic, under a specific Board  model, created by a user.
    """
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='topics')

class Post(models.Model):
    """
    Stores a single post entry which lives in a topic. Can be created and
    edited by a user.
    """
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='posts')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   null=True, related_name='+')
