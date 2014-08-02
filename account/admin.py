#-*-coding:utf-8-*-
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from account.models import Account,Profile
import sha, random

class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	email = forms.CharField(label = '', widget=forms.TextInput(attrs = {'class': 'form-control',
															'placeholder': '邮箱地址',}))
	password1 = forms.CharField(label = '', widget=forms.PasswordInput(attrs = {'class': 'form-control',
																	'placeholder': '密码',}))
	password2 = forms.CharField(label = '', widget=forms.PasswordInput(attrs = {'class': 'form-control',
																	'placeholder': '确认密码',}))

	class Meta:
		model = Account
		fields = ('email',)

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("两次密码不一致")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.register_time = datetime.now()
		#generate activation key
		email = self.cleaned_data["email"]
		salt = sha.new(str(random.random())).hexdigest()[:5]
		activation_key = sha.new(salt+email).hexdigest()
		user.activation_key = activation_key
		#send email parameters setting
		from_email = settings.EMAIL_HOST_USER
		to_email = [self.cleaned_data['email'],from_email, 'zhangbin.1101@gmail.com']
		subject = '注册成功 - TenniSoda'
		message = '恭喜您已成功注册网球苏打，请点击以下链接激活帐号。\n http://%s/account/confirm/%s' % (settings.HOST_DOMAIN, user.activation_key)
		if commit:
			#send email..
			send_mail(subject, message, from_email, to_email, fail_silently = False)
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Account
		fields = ('email', 'password', 'is_active', 'is_admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]


class AccountAdmin(UserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = UserCreationForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('id', 'email', 'is_admin', 'is_active', 'register_time', 'first_login')
	list_filter = ('is_admin', 'is_active', 'first_login')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Permissions', {'fields': ('is_admin',)}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', '__unicode__', 'gender', 'court', 'city', 'birth_date', 'level', 'phone', 'club', 'self_introduction']
	list_filter = ('city', 'gender', 'level', 'club')
	ordering = ['city', 'gender', 'level',]


# Now register the new UserAdmin...
admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
