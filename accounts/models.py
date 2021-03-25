from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from .managers import TeamManager

import datetime

class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    banner_img = models.ImageField(width_field=1920, height_field=1280, null=True, blank=True)
    score = models.IntegerField(default=0)
    
    owner = models.OneToOneField("User", on_delete=models.CASCADE, null=True,)
    members = models.ManyToManyField('User', through="Member", related_name="%(class)s_members")

    date_created = models.DateField(auto_now=True)
    date_updated = models.DateField(auto_now_add=True)
    
    objects = TeamManager()

    def __str__(self):
        return self.name
        
    def get_monthly_global(self):
        teams_month = Team.objects.raw(
            "SELECT * FROM users_teams WHERE score > 0 AND date_updated > {0};"
        ).format(datetime.timedelta(days=7))
        return teams_month

    class Meta:
        db_table = "users_teams"

class Member(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username


# Create your models here.
class User(AbstractUser):
    timezone = models.CharField(max_length=55, default='Europe/London')
    
    @property
    def team(self):
        return Team.objects.get_or_404(owner=self)

    class Meta:
        db_table = "users"
