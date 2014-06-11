from django.db import models
from account.models import Account
from game.models import Game
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length = 256)
    message = models.TextField()
    viewed = models.BooleanField(default = False)
    user = models.ForeignKey(Account)
    time = models.DateTimeField()

@receiver(post_save, sender = Account)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user = kwargs.get('instance'),
                                    title = 'Welcome to TenniSoda',
                                    message = 'Thanks for sign up in TenniSoda',
                                    time = datetime.now())

@receiver(post_save, sender = Game)
def create_game_message(sender, **kwargs):
    if kwargs.get('created', False):
        game = kwargs.get('instance')
        Notification.objects.create(user = game.player1.user,
                                    title = 'New game',
                                    message = 'You have a new game to play, go to the game page to view details',
                                    time = datetime.now())
        Notification.objects.create(user = game.player2.user,
                                    title = 'New game',
                                    message = 'You have a new game to play, go to the game page to view details',
                                    time = datetime.now())
