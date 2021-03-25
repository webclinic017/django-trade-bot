from django.db import models

# Create your models here.
class Poll(models.Model):
    first_question = models.CharField(max_length=40)
    second_question = models.CharField(max_length=40)
    name = models.CharField(blank=True, max_length=30)
    name2 = models.CharField(blank=True, max_length=30)
    