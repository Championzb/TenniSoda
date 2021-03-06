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
from django.conf import settings
from friendship.models import Friend, Follow
from django.core.paginator import Paginator
from activity.models import ActivityFeed
from admin import UserCreationForm, send_email
from datetime import datetime, date

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
			messages.success(request,u'您已经成功注册， 请去您的邮箱%s激活帐号！' % (form.cleaned_data['email']))
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
	#from_email = settings.EMAIL_HOST_USER
	#to_email = [email, from_email, 'zhangbin.1101@gmail.com']
	#subject = u'重置密码 - TenniSoda'
	#message = u'您的密码已经被重置为 %s' % (new_password)
	#send_mail(subject, message, from_email, to_email, fail_silently = True)
	send_email(u'重置密码 - TenniSoda', u'您的密码已经被重置为 %s' % (new_password), [email])
	


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
			messages.success(request, u'您的新密码已发送至 %s' % (email))
			return HttpResponseRedirect('/account/login/')


	return render_to_response('account-forgot.html', args)

def login(request):
	if request.method == 'POST':
		email = request.POST.get('email', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(email=email, password=password)

		if user is not None:
			if user.is_active:
				auth.login(request, user)
				if request.POST.getlist('remember_me'):
					request.session['email'] = email
					request.session['password'] = password
				else:
					try:
						del request.session['email']
						del request.session['password']
					except KeyError:
						pass				
				if request.POST['next']:
					return HttpResponseRedirect(request.POST['next'])
				else:
					if user.first_login:
						return HttpResponseRedirect('/account/first_login/')
					else:
						return HttpResponseRedirect('/game/league/')
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
	else:
		args = {}
		args.update(csrf(request))
		args['next'] = request.GET.get('next', '')
		return render(request, 'account-login.html', args)

@login_required
def first_login(request):
	user = request.user
	user.first_login = False
	user.save()
	'''
	notifications = Notification.objects.filter(user = request.user, viewed = False).order_by('time').reverse()

	args = {}
	args['notifications'] = notifications
	return render_to_response('account-tutorial.html', args)
	'''
	
	return HttpResponseRedirect("/game/league/")

@login_required
def welcome_user(request):
	username = request.user.email.split('@')[0]
	if request.user.profile.last_name!='' and request.user.profile.last_name is not None:
		username = request.user.profile.last_name+' '+request.user.profile.first_name

	#league_match_attended = League.objects.filter(players=request.user.profile)
	games_count = Game.objects.filter((Q(player1 = request.user) | Q(player2 = request.user))).count()
	games_win_count = Game.objects.filter(winner = request.user).count()
	notifications = Notification.objects.filter(user = request.user, viewed = False).order_by('time').reverse()
	
	followings = Follow.objects.following(request.user)
	
	activities = []
	for following in followings:
		if following.profile:
			for activity in ActivityFeed.objects.filter(creator=following).order_by('date_time').reverse():
				activities.append(activity)
				
	#activities = activities.order_by('date_time')
	activities = sorted(activities, key=lambda x: x.date_time, reverse=True)
	
	page_number = request.GET.get('page','1')
	
	profile = request.user.profile

	args = {}
	args['profile'] = profile
	args['games_count'] = games_count
	args['games_win_count'] = games_win_count
	#args['league_matches_attended'] = league_match_attended
	#args['league_matches_remained'] = League.objects.exclude(players=request.user)
	args['notifications'] = notifications
	args['followers_count'] = len(Follow.objects.followers(request.user))
	args['following_count'] = len(Follow.objects.following(request.user))
	args['activities'] = Paginator(activities, 10).page(page_number)
	args['date'] = date.today()
	return render(request, 'page-profile.html',args)

def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['password']
	except KeyError:
		pass
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
			messages.success(request,u'修改资料成功！')
			return render(request,'page-settings.html',args)
	else:
		user = request.user
		profile = user.profile
		if profile.level:
			level = profile.level
		else:
			level = '3'
		form = UserProfileForm(instance=profile, initial={'phone':profile.phone, 'picture':profile.picture, 'level': level})

	args['form'] = form
	args['email'] = request.user.email
	args['profile'] = request.user.profile

	return render(request, 'page-settings.html',args)

@login_required
def view_profile(request, user_id=1):
	user = request.user
	opponent_user = Account.objects.get(id=user_id)
	if user == opponent_user:
		return HttpResponseRedirect('/account/welcome_user/')


	games_count = Game.objects.filter((Q(player1=opponent_user) | Q(player2=opponent_user))).count()
	games_win_count = Game.objects.filter(winner=opponent_user).count()
	notifications = Notification.objects.filter(user=user, viewed=False).order_by('time').reverse()

	activities = ActivityFeed.objects.filter(creator = opponent_user).order_by('date_time').reverse()
	page_number = request.GET.get('page','1')

	args = {}
	args['profile'] = user.profile
	args['opponent_profile'] = opponent_user.profile
	args['is_followed'] = Follow.objects.follows(user, opponent_user)
	args['games_count'] = games_count
	args['games_win_count'] = games_win_count
	args['notifications'] = notifications
	args['activities'] = Paginator(activities,10).page(page_number)
	args['followers_count'] = len(Follow.objects.followers(opponent_user))
	args['following_count'] = len(Follow.objects.following(opponent_user))
	args['date'] = date.today()

	return render(request, 'view-profile.html',args)


@login_required
def change_password(request):
	user = request.user

	if request.method == 'POST':
		old_password = request.POST.get('old-password', '')
		new_password1 = request.POST.get('new-password-1', '')
		if not user.check_password(old_password):
			messages.warning(request,u'密码错误！')
			return HttpResponseRedirect('/account/change_profile/')
		else:
			user.set_password(new_password1)
			user.save()
			messages.success(request,u'成功修改密码！')
			return HttpResponseRedirect('/account/change_profile/')

	return HttpResponseRedirect('/account/change_profile/')

def confirm(request,activation_key):
	if Account.objects.filter(activation_key = activation_key).count() == 0:
		messages.warning(request, u'激活链接错误，请登录后申请重新激活帐号！')
		form = UserCreationForm()
		
		args = {}
		args.update(csrf(request))

		return render(request, 'account-login.html', args)
	else:
		user = Account.objects.get(activation_key=activation_key)
		user.is_active = True
		user.save()
		
		#messages.success(request, u'帐号已激活，请登录！')
		
		#args = {}
		#args.update(csrf(request))
		#args['email'] = user.email
		#return render(request, 'account-login.html', args)
		user.backend='django.contrib.auth.backends.ModelBackend'
		auth.login(request, user)
		return HttpResponseRedirect('/account/first_login/')



def confirmation_resend(request):
	#from_email = settings.EMAIL_HOST_USER
	#to_email = [request.session['email'],from_email, 'zhangbin.1101@gmail.com']
	#subject = u'帐号激活 - TenniSoda'
	#message = u'请点击以下链接激活帐号。\n http://%s/account/confirm/%s' % (settings.HOST_DOMAIN, request.session['activation_key'])
	#send email..
	#send_mail(subject, message, from_email, to_email, fail_silently = True)
	send_email(u'帐号激活 - TenniSoda', u'请点击以下链接激活帐号。\n http://%s/account/confirm/%s' % (settings.HOST_DOMAIN, request.session['activation_key']), [request.session['email']])
	messages.success(request,u'请去您的邮箱 %s 激活帐号' % (request.session['email']))
	return HttpResponseRedirect('/account/login/')

def add_follower(request, user_id = 1):
	user= Account.objects.get(id = user_id)
	Follow.objects.add_follower(request.user, user)
	Notification.objects.create(user = user, title = u'新增粉丝', message = u'%s 关注了您！' % (request.user.profile), time = datetime.now())
										
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_follower(request, user_id = 1):
	user = Account.objects.get(id = user_id)
	Follow.objects.remove_follower(request.user, user)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def get_followers(request, user_id = 1):
	user = request.user
	opponent_user = Account.objects.get(id=user_id)
	followers = Follow.objects.followers(opponent_user)
	games_count = Game.objects.filter((Q(player1 = opponent_user) | Q(player2 = opponent_user))).count()
	games_win_count = Game.objects.filter(winner = opponent_user).count()

	notifications = Notification.objects.filter(user=user, viewed=False).order_by('time').reverse()

	page_number = request.GET.get('page','1')

	args = {}
	args['profile'] = user.profile
	args['opponent_profile'] = opponent_user.profile
	args['games_count'] = games_count
	args['games_win_count'] = games_win_count
	args['notifications'] = notifications
	args['is_followed'] = Follow.objects.follows(user, opponent_user)
	args['followers'] = Paginator(followers,10).page(page_number)
	args['myfollowing'] = Follow.objects.following(user)
	args['followers_count'] = len(Follow.objects.followers(opponent_user))
	args['following_count'] = len(Follow.objects.following(opponent_user))
	if user == opponent_user:
		return render(request, 'view-my-followers.html',args)

	return render(request, 'view-followers.html',args)

def get_following(request, user_id = 1):
	user = request.user
	opponent_user = Account.objects.get(id=user_id)
	following = Follow.objects.following(opponent_user)
	games_count = Game.objects.filter((Q(player1 = opponent_user) | Q(player2 = opponent_user))).count()
	games_win_count = Game.objects.filter(winner = opponent_user).count()

	notifications = Notification.objects.filter(user=user, viewed=False).order_by('time').reverse()

	page_number = request.GET.get('page','1')

	args = {}
	args['profile'] = user.profile
	args['opponent_profile'] = opponent_user.profile
	args['games_count'] = games_count
	args['games_win_count'] = games_win_count
	args['notifications'] = notifications
	args['is_followed'] = Follow.objects.follows(user, opponent_user)
	args['following'] = Paginator(following,10).page(page_number)
	args['myfollowing'] = Follow.objects.following(user)
	args['followers_count'] = len(Follow.objects.followers(opponent_user))
	#args['followers_count'] = opponent_user.get_followers_num()
	args['following_count'] = len(Follow.objects.following(opponent_user))

	if user == opponent_user:
		return render(request, 'view-my-following.html',args)

	return render(request, 'view-following.html',args)

def search(request):
	user = request.user
	games_count = Game.objects.filter((Q(player1 = request.user) | Q(player2 = request.user))).count()
	games_win_count = Game.objects.filter(winner = request.user).count()
	notifications = Notification.objects.filter(user=user, viewed=False).order_by('time').reverse()

	keyword=request.GET.get('keyword','')

	following = Follow.objects.following(user)
	page_number = request.GET.get('page','1')

	has_match = False
	profile_set = Profile.objects.all()
	for word in keyword:
		if profile_set.filter(Q(first_name__contains=word)|Q(last_name__contains=word)):
			profile_set = profile_set.filter(Q(first_name__contains=word)|Q(last_name__contains=word))
			has_match = True
		else:
			continue
			
	search_result = []
	search_result.extend(list(profile_set))
	
	if keyword:
		account = Account.objects.all().filter(email=keyword)
		if account.count() > 0:
			has_match = True
			search_result = []
			search_result.append(account[0].profile)
		
	args = {}
	args.update(csrf(request))
	args['profile'] = user.profile
	args['games_count'] = games_count
	args['games_win_count'] = games_win_count
	args['notifications'] = notifications
	args['search_result'] = Paginator(search_result, 20).page(page_number)
	args['followers_count'] = len(Follow.objects.followers(request.user))
	args['following_count'] = len(Follow.objects.following(request.user))
	args['following'] = following
	args['has_match'] = has_match

	return render(request, 'search-result.html', args)

def display_all_users(request):
	user = request.user
	#all_users = Account.objects.all().exclude(id = user.id)
	all_users = []
	
	profile_set = Profile.objects.all()	
	set_with_img = profile_set.exclude(picture__isnull=True).exclude(picture__exact='').order_by('user__last_login').reverse()
	#set_with_phone = profile_set.exclude(user_id__in=set_with_img).exclude(phone__isnull=True).exclude(phone__exact='').order_by('user__last_login')
	set_with_phone = profile_set.filter(Q(picture__isnull=True)|Q(picture__exact='')).exclude(phone__isnull=True).exclude(phone__exact='').order_by('user__last_login').reverse()
	#set_all = profile_set.exclude(user_id__in=set_with_img).exclude(user_id__in=set_with_phone)
	set_all = profile_set.filter((Q(picture__isnull=True)|Q(picture__exact='')),(Q(phone__isnull=True)|Q(phone__exact=''))).reverse()
	all_users.extend(list(set_with_img))
	all_users.extend(list(set_with_phone))
	all_users.extend(list(set_all))
	
	notifications = Notification.objects.filter(user=user, viewed=False).order_by('time').reverse()
	page_number = request.GET.get('page','1')
	following = Follow.objects.following(user)
	
	
	args = {}
	args['all_users'] = Paginator(all_users, 16).page(page_number)
	args['profile'] = user.profile
	args['notifications'] = notifications
	args['following'] = following

	return render(request, 'all-users.html',args)
	

