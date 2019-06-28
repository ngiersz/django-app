from django.db import models
from django.utils import timezone


class Order(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(default='')
    created_date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.title


