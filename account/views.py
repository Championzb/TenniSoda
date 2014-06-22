from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth, messages
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from forms import UserProfileForm
from game.models import League, Game
from models import Profile, Account
from notification.models import Notification


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
			#messages.success(request,'You have registered successfully.')
			return HttpResponseRedirect('/account/login')
	else:
		form = UserCreationForm()

	args = {}
	args.update(csrf(request))

	args['form'] = form

	return render_to_response('account-signup.html', args)

def login(request):
	args = {}
	args.update(csrf(request))
	return render_to_response('account-login.html', args)

def auth_view(request):
	email = request.POST.get('email', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(email=email, password=password)

	print "--------------"
	print email

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/account/welcome_user/')
	else:
		return HttpResponseRedirect('/account/invalid_login/')

@login_required
def welcome_user(request):
	username = request.user.email.split('@')[0]
	if request.user.profile.last_name!='' and request.user.profile.last_name is not None:
		username = request.user.profile.last_name+request.user.profile.first_name
	league_match_attended = League.objects.filter(players=request.user.profile)

	notifications = Notification.objects.filter(user = request.user, viewed = False)

	profile = request.user.profile

	args = {}
	args['username'] = username
	args['profile'] = profile
	args['league_matches_attended'] = league_match_attended
	args['league_matches_remained'] = League.objects.exclude(players=request.user)
	args['notifications'] = notifications
	return render_to_response('page-profile.html',args)

def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	auth.logout(request)

	args = {}
	args.update(csrf(request))
	#messages.success(request,'You have logged out successfully!')
	return HttpResponseRedirect('/')

@login_required
def change_profile(request):
	args = {}
	args.update(csrf(request))
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance = request.user.profile,)
		if form.is_valid():
			form.save()
			#messages.success(request,'You have updated the profile')
			args['form'] = form
			args['email'] = request.user.email
			args['profile'] = request.user.profile
			return render(request,'page-settings.html',args)
	else:
		user = request.user
		profile = user.profile
		form = UserProfileForm(instance=profile,initial={'phone':profile.phone})	


	
	args['form'] = form
	args['email'] = request.user.email
	args['profile'] = request.user.profile
	
	return render(request, 'page-settings.html',args)

@login_required
def view_profile(request, user_id=1):
	user = request.user.profile
	opponent_profile = Profile.objects.get(user_id=user_id)
	if Game.objects.filter(player1=user,player2=opponent_profile).count() == 0 and Game.objects.filter(player2=user,player1=opponent_profile).count() == 0:
		return HttpResponseRedirect('/game/list_all_games')
	args = {}
	args['email']= Account.objects.get(id = user_id).email
	args['first_name'] = opponent_profile.first_name
	args['last name'] = opponent_profile.last_name
	args['phone'] = opponent_profile.phone
	args['level'] = opponent_profile.level
	return render_to_response('view_profile.html',args)


@login_required
def change_password(request):
	user = request.user

	if request.method == 'POST':
		old_password = request.POST.get('old-password', '')
		new_password1 = request.POST.get('new-password-1', '')
		if not user.check_password(old_password):
			messages.warning(request,'Invalid Password!')
			return HttpResponseRedirect('/account/change_profile/')
		else:
			user.set_password(new_password1)
			user.save()
			messages.success(request,'Change Password Successfully.')
			return HttpResponseRedirect('/account/change_profile/')

	return HttpResponseRedirect('/account/change_profile/')


