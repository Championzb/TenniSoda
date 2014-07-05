from django.db import models
from city.models import City
from geoposition.fields import GeopositionField
from TenniSoda import settings
from time import time

def get_upload_file_name(instance, filename):
	return settings.UPLOAD_FILE_PATTERN % ('court_pic', str(time()).replace('.','_'), filename)

class Court(models.Model):
	name = models.CharField(max_length=50)
	city = models.ForeignKey(City, null=False, blank=False)
	address = models.CharField(max_length=200)
	fee = models.IntegerField()
	picture = models.ImageField(upload_to = get_upload_file_name, null=True, blank=True)
	position = GeopositionField()
	phone = models.CharField(max_length=11, null=True,blank=True)
	#is_free = models.BooleanField()

	def __unicode__(self):
		return self.name
	
