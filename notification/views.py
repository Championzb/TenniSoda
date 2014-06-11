from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import Notification

# Create your views here.
def show(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    return render_to_response('notification.html',{'notification':notification})

def mark_as_viewed(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.viewed = True
    notification.save()

    return HttpResponseRedirect('/account/welcome_user')
