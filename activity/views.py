from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import ActivityFeed

# Create your views here.

def like(request, activityFeed_id):
	activity = ActivityFeed.objects.get(id=activityFeed_id)
	activity.like_num += 1
	activity.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
