from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import Notification
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def show(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    return render_to_response('notification.html',{'notification':notification})

@login_required
def mark_as_viewed(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.viewed = True
    notification.save()

    return HttpResponseRedirect('/notification/all/')

@login_required
def all(request):
    """

    show user all notifications
    :param request:
    :return:
    """
    profile = request.user.profile
    notifications = Notification.objects.filter(user = request.user).order_by('time').reverse()
    #notifications_viewed = Notification.objects.filter(user = request.user, viewed=True).order_by('time').reverse()
    #notifications_not_viewed = Notification.objects.filter(user = request.user, viewed=False).order_by('time').reverse()

    args = {}
    args['profile'] = profile
    args['notifications'] = notifications
    #args['notifications_viewed'] = notifications_viewed
    #args['notifications_not_viewed'] = notifications_not_viewed

    return render_to_response('page-notifications.html', args)