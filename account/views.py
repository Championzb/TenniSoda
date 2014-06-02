from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf

from admin import UserCreationForm

import logging

logr = logging.getLogger(__name__)

# Create your views here.
def register_user(request):
    """

    For user register a account
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account/register_success')
    else:
        form = UserCreationForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('register.html', args)

def register_success(ruquest):
    return render_to_response('register_success.html')