from django.db import models

from .managers import CoinManager

class Coin(models.Model):
    name = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)
    icon = models.ImageField()
    
    objects = CoinManager()

    def __str__(self):
        return self.name
    

    class Meta:
        db_table = "crypto_coins"