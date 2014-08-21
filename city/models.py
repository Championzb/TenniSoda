from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length = 20, null = False, blank = False)

    def __unicode__(self):
        return self.name

class District(models.Model):
    city = models.ForeignKey(City, null = False, blank = False)
    name = models.CharField(max_length = 20, null = False, blank = False)

    class Meta:
        unique_together = ('city', 'name',)

    def __unicode__(self):
        return u"%s %s" % (self.name)
