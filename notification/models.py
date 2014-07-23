#-*-coding:utf-8-*-
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
                                    title = '欢迎来到网球苏打',
                                    message = '感谢您注册网球苏打',
                                    time = datetime.now())

@receiver(post_save, sender = Game)
def create_game_message(sender, **kwargs):
    if kwargs.get('created', False):
        game = kwargs.get('instance')
        Notification.objects.create(user = game.player1.user,
                                    title = '新的比赛',
                                    message = '您有一场新的比赛，请去比赛页面查看比赛详情',
                                    time = datetime.now())
        Notification.objects.create(user = game.player2.user,
                                    title = '新的比赛',
                                    message = '您有一场新的比赛，请去比赛页面查看比赛详情',
                                    time = datetime.now())
