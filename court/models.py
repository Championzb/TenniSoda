from django.db import models

class Court(models.Model):
	name = models.CharField(max_length=50)
	city = models.CharField(max_length=10)
	address = models.CharField(max_length=200)
	is_free = models.BooleanField()

	
	def __unicode__(self):
		return self.name
	

