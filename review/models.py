from django.db import models
from account.models import Profile
from court.models import Court
from game.models import Game
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class CourtReview(models.Model):
    game = models.ForeignKey(Game, blank = True, null = True)
    court = models.ForeignKey(Court)
    player = models.ForeignKey(Profile)
    review = models.TextField(max_length = 1000, blank = True, null = True)
    rate = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)],blank = True, null = True)
    reviewed_time = models.DateTimeField(blank = True, null = True)

    class Meta:
        unique_together = ('game', 'player', )

    def __unicode__(self):
        name = u"%s " % self.court + u"%s " % self.user
        return name

class RateReview(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Profile)
    rate = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)], blank = True, null = True)
    review = models.TextField(max_length = 1000, blank = True, null = True)
    reviewed_time = models.DateTimeField(blank = True, null = True)

    class Meta:
        unique_together = ('game', 'player', )

    def __unicode__(self):
        return u'%s %s' % (self.game, self.player)
