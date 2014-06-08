from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from forms import UserProfileForm
from game.models import League
from models import Profile


from admin import UserCreationForm

import logging

#logr = logging.getLogger(__name__)

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

def login(request):
	args = {}
	args.update(csrf(request))
	return render_to_response('login.html', args)

def auth_view(request):
	email = request.POST.get('email', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(email=email, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/account/welcome_user')
	else:
		return HttpResponseRedirect('/account/invalid_login')

@login_required
def welcome_user(request):
	username = request.user.email.split('@')[0]
	if request.user.profile.last_name!='' and request.user.profile.last_name is not None:
		username = request.user.profile.last_name+request.user.profile.first_name
	league_match_attended = League.objects.filter(players=request.user.profile)
	return render_to_response('welcome_user.html',{'username':username,'league_matches_attended':league_match_attended,'league_matches_remained': League.objects.exclude(players=request.user),})

def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	auth.logout(request)

	args = {}
	args.update(csrf(request))

	return render_to_response('login.html', args)

@login_required
def change_profile(request):
	if request.method == 'POST':
		form = UserProfileForm(request.POST, instance = request.user.profile,)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/account/welcome_user')
	else:
		user = request.user
		profile = user.profile
		form = UserProfileForm(instance=profile,initial={'phone':profile.phone})	

	args = {}
	args.update(csrf(request))
	
	args['form'] = form
	
	return render_to_response('profile.html',args)
