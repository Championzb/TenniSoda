from django.db import models
from account.models import Profile
from game.models import GameGroup, League, Game
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class ActivityFeed(models.Model):
    type = models.IntegerField(default = 0) #1 for hold game_group; 2 for join game_group; 3 for join league; 4 for win game
    date_time = models.DateTimeField(default = datetime.now())
    creator = models.ForeignKey(Profile)
    game_group = models.ForeignKey(GameGroup, blank = True, null = True)
    league = models.ForeignKey(League, blank = True, null = True)
    game = models.ForeignKey(Game, blank = True, null = True)
    like_num = models.IntegerField(default = 0)

    def __unicode__(self):
        return u'%s %s %s' % (self.type, self.date_time, self.creator)

@receiver(post_save, sender = GameGroup)
def create_gamegroup_activityfeed(sender, **kwargs):
    game_group = kwargs.get('instance')
    if kwargs.get('created', False):
        ActivityFeed.objects.create(type = '1',
                                    date_time = datetime.now(),
                                    creator = game_group.holder,
                                    game_group = game_group)
