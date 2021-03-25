from django.db import models

class CoinManager(models.Manager):
    use_for_related_fields = False

    def create_coin(self, name, full_name, icon):
        '''Create singular coin'''
        pass
    def create_coins(self, data):
        '''Create coins from array of data'''
        pass
    def remove_coin(self, name):
        pass