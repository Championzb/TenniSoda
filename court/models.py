from django.db import models
from city.models import City

class Court(models.Model):
	name = models.CharField(max_length=50)
	city = models.ForeignKey(City, null=False, blank=False)
	address = models.CharField(max_length=200)
	is_free = models.BooleanField()

	
	def __unicode__(self):
		return self.name
	

