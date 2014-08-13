#-*-coding:utf-8-*-
from django import forms
from models import Profile
from court.models import Court
from city.models import City, District
from django.forms import extras
from localflavor.cn.forms import CNCellNumberField, CNProvinceSelect
from django.contrib.admin.widgets import AdminDateWidget
from bootstrap3_datetime.widgets import DateTimePicker
from form_utils.widgets import ImageWidget


LEVEL=(('1','1 (入门)'),('1.5','1.5'),('2','2'),('2.5','2.5'),('3','3'),('3.5','3.5(进阶)'),('4','4'),('4.5','4.5'),('5','5'),('5.5','5.5(高手)'))
GENDER=(('1','男'),('0','女'))

class UserProfileForm(forms.ModelForm):
	last_name = forms.CharField(widget=forms.TextInput(attrs = {'class': 'form-control'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs = {'class': 'form-control'}))
	level = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}), choices=LEVEL, required=False, )
	gender = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=GENDER,required=False)
	city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs = {'class': 'form-control', 'id': 'city'}), required=False)
	district = forms.ModelChoiceField(queryset=District.objects.all(), widget=forms.Select(attrs = {'class': 'form-control', 'id': 'district'}), required=False)
	phone = CNCellNumberField(widget=forms.TextInput(attrs = {'class': 'form-control'}), required=False)
	birth_date = forms.DateField(widget=forms.DateInput(attrs = {'class': 'form-control','type':'date'}), required=False)
	#birth_date = forms.DateField(widget=DateTimePicker(options = {"format": "YYYY-MM-DD", "picktime": True}, attrs = {'id': 'datetimepicker'}), required=False)
	court = forms.ModelChoiceField(queryset=Court.objects.all(), widget=forms.Select(attrs = {'class': 'form-control'}), required=False)
	picture = forms.ImageField(widget=ImageWidget(attrs = {'class': 'form-control'}), required=False)
	club = forms.CharField(widget=forms.TextInput(attrs = {'class': 'form-control'}), required = False)
	self_introduction = forms.CharField(widget=forms.Textarea(attrs = {'class': 'form-control'}), required = False)


	class Meta:
		model = Profile
		#fields = ('picture', 'last_name','first_name','gender','city', 'district', 'birth_date','court','level')
		fields = ('last_name','first_name','gender','city', 'district', 'birth_date','court','level', 'club', 'self_introduction')

	def save(self,commit=True):
		form = super(UserProfileForm,self).save(commit=False)
		form.phone = self.cleaned_data['phone']
		if self.cleaned_data['picture'] is not None:
			form.picture = self.cleaned_data['picture']
		if commit:
			form.save()

		return form
		
	def clean_picture(self):
		picture = self.cleaned_data.get('picture', False)
		if picture:
			if picture._size > 4*1024*1024:
				raise forms.ValidationError("图片尺寸不得超过4M")
			return picture
