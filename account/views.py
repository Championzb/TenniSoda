#-*-coding:utf-8-*-
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth, messages
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from forms import UserProfileForm
from game.models import League, Game
from models import Profile, Account
from notification.models import Notification
from django.db.models import Q
from django.template import RequestContext
from django.core.mail import send_mail
from django.conf import settings
from friendship.models import Friend, Follow


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
			messages.success(request,'您已经成功注册， 请去您的邮箱%s激活帐号！' % (form.cleaned_data['email']))
			return HttpResponseRedirect('/account/login/')
	else:
		form = UserCreationForm()

	args = {}
	args.update(csrf(request))

	args['form'] = form

	return render_to_response('account-signup.html', args)

#reset password
def reset_password(email):
	user = Account.objects.get(email = email)
	new_password = Account.objects.make_random_password()
	print 'new password: %s' % new_password
	user.set_password(new_password)
	user.save()
	from_email = settings.EMAIL_HOST_USER
	to_email = [email, from_email, 'zhangbin.1101@gmail.com']
	subject = '重置密码 - TenniSoda'
	message = '您的密码已经被重置为 %s' % (new_password)
	send_mail(subject, message, from_email, to_email, fail_silently = True)


#forget password view
def forget_password(request):
	args = {}
	args.update(csrf(request))
	args['warning'] = False
	if request.method == 'POST':
		email = request.POST.get('email','')
		print email
		if Account.objects.filter(email=email).count() == 0:
			print 'no such user'
			args['warning'] = True

			return render_to_response('account-forgot.html',args)
		else:
			print 'reset password'
			reset_password(email)
			messages.success(request, '您的新密码已发送至 %s' % (email))
			return HttpResponseRedirect('/account/login/')


	return render_to_response('account-forgot.html', args)

def login(request):
	args = {}
	args.update(csrf(request))
	return render(request, 'account-login.html', args)

def auth_view(request):
	email = request.POST.get('email', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(email=email, password=password)

	if user is not None:
		if user.is_active:
			auth.login(request, user)
			if user.first_login:
				return HttpResponseRedirect('/account/first_login/')
			else:
				return HttpResponseRedirect('/account/welcome_user/')
		else:
			args = {}
			request.session['email'] = email
			request.session['activation_key'] = user.activation_key
			return render_to_response('require-active.html', args, context_instance=RequestContext(request))
	else:
		args = {}
		args.update(csrf(request))
		args['warning'] = True
		args['email_exist'] = False
		if Account.objects.filter(email=email).count() != 0:
			args['email_exist'] = True
		else:
			args['email_exist'] = False
		return render(request, 'account-login.html', args)

@login_required
def first_login(request):
	user = request.user
	user.first_login = False
	user.save()
	notifications = Notification.objects.filter(user = request.user, viewed = False).order_by('time').reverse()

	args = {}
	args['notifications'] = notifications
	return render_to_response('account-tutorial.html', args)

@login_required
def welcome_user(request):
	username = request.user.email.split('@')[0]
	if request.user.profile.last_name!='' and request.user.profile.last_name is not None:
		username = request.user.profile.last_name+' '+request.user.profile.first_name

	#league_match_attended = League.objects.filter(players=request.user.profile)
	games_count = Game.objects.filter((Q(player1 = request.user) | Q(player2 = request.user))).count()
	games_win_count = Game.objects.filter(winner = request.user).count()
	notifications = Notification.objects.filter(user = request.user, viewed = False).order_by('time').reverse()

	profile = request.user.profile

	args = {}
	args['username'] = username
	args['profile'] = profile
	args['games_count'] = games_count
	args['games_win_count'] = games_win_count
	#args['league_matches_attended'] = league_match_attended
	#args['league_matches_remained'] = League.objects.exclude(players=request.user)
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
	notifications = Notification.objects.filter(user = request.user, viewed = False).order_by('time').reverse()
	args = {}
	args.update(csrf(request))
	args['notifications'] = notifications
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance = request.user.profile,)
		if form.is_valid():
			form.save()
			#request.user.profile.picture = form.cleaned_data['picture']
			#request.user.profile.save()
			#messages.success(request,'You have updated the profile')
			args['form'] = form
			args['email'] = request.user.email
			args['profile'] = request.user.profile
			return render(request,'page-settings.html',args)
	else:
		user = request.user
		profile = user.profile
		form = UserProfileForm(instance=profile, initial={'phone':profile.phone, 'picture':profile.picture})

	args['form'] = form
	args['email'] = request.user.email
	args['profile'] = request.user.profile

	return render(request, 'page-settings.html',args)

@login_required
def view_profile(request, user_id=1):
	user = request.user
	opponent_user = Account.objects.get(user_id=user_id)
	if user == opponent_user:
		return HttpResponseRedirect('/account/welcome_user/')

	notifications = Notification.objects.filter(user=user, viewed=False).order_by('time').reverse()

	args = {}
	args['profile'] = user.profile
	args['opponent_profile'] = opponent_user.profile
	args['is_followed'] = Follow.objects.follows(user, opponent_user)
	args['notifications'] = notifications

	return render_to_response('view-profile.html',args)


@login_required
def change_password(request):
	user = request.user

	if request.method == 'POST':
		old_password = request.POST.get('old-password', '')
		new_password1 = request.POST.get('new-password-1', '')
		if not user.check_password(old_password):
			messages.warning(request,'密码错误！')
			return HttpResponseRedirect('/account/change_profile/')
		else:
			user.set_password(new_password1)
			user.save()
			messages.success(request,'成功修改密码！')
			return HttpResponseRedirect('/account/change_profile/')

	return HttpResponseRedirect('/account/change_profile/')

def confirm(request,activation_key):
	if Account.objects.filter(activation_key = activation_key).count() == 0:
		messages.warning(request, '激活链接错误，请重新申请激活帐号！')
		return HttpResponseRedirect('/')
	else:
		user = Account.objects.get(activation_key=activation_key)
		user.is_active = True
		user.save()
		messages.success(request, '帐号已激活，请登录！')
		args = {}
		args.update(csrf(request))
		args['email'] = user.email
		return render(request, 'account-login.html', args)



def confirmation_resend(request):
	from_email = settings.EMAIL_HOST_USER
	to_email = [request.session['email'],from_email, 'zhangbin.1101@gmail.com']
	subject = '帐号激活 - TenniSoda'
	message = '请点击以下链接激活帐号。\n http://%s/account/confirm/%s' % (settings.HOST_DOMAIN, request.session['activation_key'])
	#send email..
	send_mail(subject, message, from_email, to_email, fail_silently = True)

	messages.success(request,'请去您的邮箱 %s 激活帐号' % (request.session['email']))
	return HttpResponseRedirect('/account/login/')

def add_follower(request, user_id = 1):
	user= Account.objects.get(id = user_id)
	Follow.objects.add_follower(request.user, user)

	return HttpResponseRedirect('/account/welcome_user/')

def remove_follower(request, user_id = 1):
	user = Account.objects.get(id = user_id)
	Follow.objects.remove_follower(request.user, user)

	return HttpResponseRedirect('/account/welcome_user/')
