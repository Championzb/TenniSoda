from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from models import Court
from notification.models import Notification

# Create your views here.

@login_required
def all(request):
    '''

    To list all the court
    :param request:
    :return:
    '''
    courts = Court.objects.all()
    user = request.user.profile
    notifications = Notification.objects.filter(user = request.user, viewed = False).order_by('time').reverse()
    args = {}
    args['courts'] = courts
    args['profile'] = user
    args['notifications'] = notifications

    return render(request, 'all-court.html', args)
