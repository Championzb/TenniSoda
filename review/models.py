from django.db import models
from account.models import Profile
from court.models import Court
# Create your models here.
class CourtReview(models.Model):
    court = models.ForeignKey(Court)
    user = models.ForeignKey(Profile)
    review = models.TextField(max_length = 1000)
    rate = models.IntegerField()

    def __unicode__(self):
        name = u"%s " % self.court + u"%s " % self.user
        return name