from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone

import datetime

from .managers import TeamManager

# teams


class Member(models.Model):
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, )
    team = models.ForeignKey("Team", on_delete=models.DO_NOTHING, )

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "users_teams_members"


class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    banner_img = models.ImageField(width_field=1920, height_field=1280, null=True, blank=True)
    score = models.IntegerField(default=0)
    
    public = models.BooleanField(default=True, )
    owner = models.ForeignKey("User", on_delete=models.DO_NOTHING,   )

    date_created = models.DateField(auto_now=True)
    date_updated = models.DateField(auto_now_add=True)
    
    objects = TeamManager()

    def __str__(self):
        return self.name

    @property
    def members(self):
        '''        get members from team         '''
        members = Member.objects.filter(team=self)

        return members
    
    @staticmethod
    def get_daily_global(score: int=0):
        '''
        Get daily teams by score
        
        @param score int
        '''

        date = datetime.datetime.now()
        date = date.replace(hour=0)

        query = "SELECT * FROM users_teams WHERE score > {1} AND date_updated > {0};".format(
            date.strftime('%x'),
            score
        )

        teams_month = Team.objects.raw(query)
        return teams_month 
    
    @staticmethod
    def get_weekly_global():
        '''Get weekly teams by score'''
        date = datetime.datetime.now()
        date = date.replace(day=7)

        query = "SELECT * FROM users_teams WHERE score > 0 AND date_updated > {0};".format(
            date.strftime('%x')
        )

        teams_month = Team.objects.raw(query)
        return teams_month 
    
    @staticmethod
    def get_monthly_global():
        '''Get monthly teams by score'''
        date = datetime.datetime.now()
        date = date.replace(day=1)

        query = "SELECT * FROM users_teams WHERE score > 0 AND date_updated > {0};".format(
            date.strftime('%x')
        )

        teams_month = Team.objects.raw(query)
        return teams_month


    class Meta:
        db_table = "users_teams"


class Referee(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "users_refered"

class User(AbstractUser):
    timezone = models.CharField(max_length=55, default='Europe/London')

    @property
    def team(self):
        try:
            member = Member.objects.get(user=self)
            team = member.team
        except Member.DoesNotExist:
            team = None

        return team
    
    @property
    def referees(self):
        '''Return refered users by current user'''
        try:
            referees = Referee.objects.get(owner=self)
        except Referee.DoesNotExist:
            referees = None
        return referees
    

    class Meta:
        db_table = "users"
