from django.db import models

class TeamManager(models.Manager):
    use_for_related_fields = True

    def create_team(self, user, team):
        # ... your code here ...
        team.owner = user
        team.members.add(user)
        team.save()
    def add_members(self, user, team):
        team.members.add(user)
    def remove_member(self, user, team):
        team.members.remove(user)
    def transfer_member(self, user, team):
        '''@TODO: transferring in progress'''
        pass

