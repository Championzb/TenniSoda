from django.db import models
from account.models import Profile
from city.models import City, District
from court.models import Court
from TenniSoda import settings
from time import time
from datetime import datetime

#get league picture name
def get_upload_file_name(instance, filename):
    return settings.UPLOAD_FILE_PATTERN % ('league_pic', str(time()).replace('.','_'), filename)
# Create your models here.
class League(models.Model):
    '''
    Define the league
    '''
    name = models.CharField(max_length = 200)
    city = models.ForeignKey(City)
    start_date = models.DateField()
    end_date = models.DateField()
    current_player_number = models.IntegerField(default = 0)
    max_player_number = models.IntegerField()
    players = models.ManyToManyField(Profile, blank = True, null = True)
    level_low = models.FloatField()
    level_high = models.FloatField()
    picture = models.ImageField(upload_to = get_upload_file_name, null=True, blank=True)
    is_finished = models.BooleanField(default=False)

    def get_players(self):
        return self.players.all()

    def __unicode__(self):
        return self.name

class Game(models.Model):
    '''
    Define the single game
    league to link the league, and null represents the ladder game
    '''
    league = models.ForeignKey(League, blank = True, null = True)
    court = models.ForeignKey(Court, blank = True, null = True)
    player1 = models.ForeignKey(Profile, related_name = 'player1')
    player2 = models.ForeignKey(Profile, related_name = 'player2')
    winner = models.ForeignKey(Profile, related_name = 'winnner', blank = True, null = True)
    date = models.DateField(blank = True, null = True)
    is_played = models.BooleanField(default = False)
    player1_confirmed = models.BooleanField(default=False)
    player2_confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        name = u"%s " % self.league+u"%s " % self.player1+u"%s " % self.player2
        return name

class Score(models.Model):
    '''
    Define the score of every single game
    '''
    game = models.OneToOneField(Game, primary_key = True)
    score11 = models.IntegerField(blank = True, null = True)
    score12 = models.IntegerField(blank = True, null = True)
    score21 = models.IntegerField(blank = True, null = True)
    score22 = models.IntegerField(blank = True, null = True)
    score31 = models.IntegerField(blank = True, null = True)
    score32 = models.IntegerField(blank = True, null = True)
    score41 = models.IntegerField(blank = True, null = True)
    score42 = models.IntegerField(blank = True, null = True)
    score51 = models.IntegerField(blank = True, null = True)
    score52 = models.IntegerField(blank = True, null = True)
    set1 = models.IntegerField(blank = True, null = True)
    set2 = models.IntegerField(blank = True, null = True)


    def __unicode__(self):
        return u"%s " % self.game

Game.score = property(lambda g: Score.objects.get_or_create(game=g)[0])

class GroupStage(models.Model):
    '''
    Define the League's group list, every league+group_number+member_number can link a unique player
    '''
    league = models.ForeignKey(League)
    group_number = models.IntegerField()
    member_number = models.IntegerField()
    player = models.ForeignKey(Profile)
    points = models.IntegerField(blank = True, null = True)

    class Meta:
        unique_together = ('league','group_number','member_number',)

    def __unicode__(self):
        return u"%s %s %s %s" % (self.league, self.group_number, self.member_number, self.player)

class FreeLeagueGame(models.Model):
    '''
    Define the request to attend a ladder game
    '''
    player = models.ForeignKey(Profile,primary_key = True)
    request_time = models.DateTimeField(default = datetime.now())

    def __unicode__(self):
        return u'%s' % self.player

class GameGroup(models.Model):
    holder = models.ForeignKey(Profile,blank = True, null = True)
    maximum = models.IntegerField(default = 4)
    current_num = models.IntegerField(default = 1)
    city = models.ForeignKey(City,blank = True, null = True)
    district = models.ForeignKey(District, blank = True, null = True)
    court = models.ForeignKey(Court, blank = True, null = True)
    date = models.DateField(default = datetime.now().today)
    start_time = models.TimeField(default = datetime.now().time)
    last_hour = models.IntegerField(default = 2)
    time = models.DateTimeField(default = datetime.now())
    level_high = models.FloatField(default=7.0)
    level_low = models.FloatField(default=2.0)
    #age_high = models.IntegerField(blank = True, null = True)
    #age_low = models.IntegerField(blank = True, null = True)
    price = models.IntegerField(default = 0)
    #gender = models.CharField(max_length = 2, default = '2')
    #is_published = models.BooleanField(default = False)
    members = models.ManyToManyField(Profile, blank = True, null = True, related_name='members')
    description = models.CharField(max_length = 140, default = 'Looking for interesting guys' )

    def __unicode__(self):
        return u'%s %s %s' % (self.holder, self.court, self.time)

    def get_members(self):
        return self.members.all()

    def get_members_list(self):
        return "\n".join([u'%s %s' % (p.first_name, p.last_name) for p in self.members.all()])

class JoinLeagueRequest(models.Model):
    '''
    Define the request to join a league
    '''
    player = models.ForeignKey(Profile,primary_key = True)
    request_time = models.DateTimeField(default = datetime.now())

    def __unicode__(self):
        return u'%s' % self.player
