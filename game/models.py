from django.db import models
from account.models import Profile
from city.models import City
from court.models import Court
from review.models import CourtReview
# Create your models here.
class League(models.Model):
    name = models.CharField(max_length = 200)
    city = models.ForeignKey(City)
    start_date = models.DateField()
    end_date = models.DateField()
    current_player_number = models.IntegerField(default = 0)
    max_player_number = models.IntegerField()
    players = models.ManyToManyField(Profile, blank = True, null = True)
    level_low = models.FloatField()
    level_high = models.FloatField()

    def __unicode__(self):
        return self.name

class Game(models.Model):
    league = models.ForeignKey(League, blank = True, null = True)
    court = models.ForeignKey(Court, blank = True, null = True)
    player1 = models.ForeignKey(Profile, related_name = 'player1')
    player2 = models.ForeignKey(Profile, related_name = 'player2')
    winner = models.ForeignKey(Profile, related_name = 'winnner')
    date = models.DateField()
    player1_rated = models.IntegerField()
    player2_rated = models.IntegerField()
    player1_reviewed = models.TextField(max_length = 1000, blank = True, null = True)
    player2_reviewed = models.TextField(max_length = 1000, blank = True, null = True)
    court_review1 = models.ForeignKey(CourtReview, related_name = 'court_review1', blank = True, null = True)
    court_review2 = models.ForeignKey(CourtReview, related_name = 'court_review2', blank = True, null = True)

    def __unicode__(self):
        name = u"%s " % self.league+u"%s " % self.player1+u"%s " % self.player2
        return name

class Score(models.Model):
    game = models.OneToOneField(Game, primary_key = True)
    score11 = models.IntegerField()
    score12 = models.IntegerField()
    score21 = models.IntegerField()
    score22 = models.IntegerField()
    score31 = models.IntegerField()
    score32 = models.IntegerField()
    score41 = models.IntegerField(blank = True, null = True)
    score42 = models.IntegerField(blank = True, null = True)
    score51 = models.IntegerField(blank = True, null = True)
    score52 = models.IntegerField(blank = True, null = True)
    is_confirmed = models.BooleanField(default=False)

    

    def __unicode__(self):
        return u"%s " % self.game

Game.score = property(lambda g: Score.objects.get_or_create(game=g)[0])

class GroupStage(models.Model):
    league = models.ForeignKey(League)
    group_number = models.IntegerField()
    member_number = models.IntegerField()
    player = models.ForeignKey(Profile)
    points = models.IntegerField(blank = True, null = True)

    def __unicode__(self):
        return u"%s %s %s" % (self.league, self.group_number, self.member_number)
