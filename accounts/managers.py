from django.db import models
from django.apps import apps

class TeamManager(models.Manager):
    use_for_related_fields = True

    @staticmethod
    def create_team(user, team):
        from .models import Member
        # ... your code here ...
        team.owner = user

        member = Member()
        member.user = user
        member.team = team

        team.save()
        member.save()

        return team

    @staticmethod
    def add_member(user, team):
        from .models import Member

        member = Member()
        member.user = user
        member.team = team
        
        member.save()

        return member
    
    @staticmethod
    def remove_member(user, team):
        members = team.members
        for member in members:

            #match found, destroying.
            if member.user is user:
                member.destroy()
        
        return team
    
    @staticmethod
    def transfer_member(user, team):
        '''@TODO: transferring in progress'''
        pass

