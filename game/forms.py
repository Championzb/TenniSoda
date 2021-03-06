#-*-coding:utf-8-*-
from django import forms
from models import Score, Game, GameGroup
from django.forms import extras
from django.forms.widgets import DateTimeInput
from court.models import Court
from city.models import City, District
from account.forms import LEVEL
from datetime import date, timedelta, datetime

SET_SCORE = ('60','61','62','63','64','75','57','76','67','06','16','26','36','46',)
SCORE = (('0', '0'),('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),)
GENDER=(('2', '男女不限'), ('1','Male'),('0','Female'))

class GameEditForm(forms.ModelForm):
	date = forms.DateField(widget=forms.DateInput(attrs = {'class': 'form-control','type':'date'}))
	court = forms.ModelChoiceField(queryset=Court.objects.all(), widget=forms.Select(attrs = {'class': 'form-control'}), required=False)

	class Meta:
		model = Game
		fields = ('court', 'date')

class ScoreCreationForm(forms.ModelForm):
	player1_set_point = 0
	player2_set_point = 0
	score11 = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=SCORE)
	score12 = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=SCORE)
	score21 = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=SCORE)
	score22 = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=SCORE)
	score31 = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=SCORE,required=False)
	score32 = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=SCORE,required=False)
	score41 = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=SCORE,required=False)
	score42 = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=SCORE,required=False)
	score51 = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=SCORE,required=False)
	score52 = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=SCORE,required=False)

	class Meta:
		model = Score
		fields = ('score11','score12','score21','score22','score31','score32','score41','score42','score51','score52',)


	def clean(self):
		cleaned_data = super(ScoreCreationForm,self).clean()
		score11 = self.cleaned_data['score11']
		score12 = self.cleaned_data['score12']
		score21 = self.cleaned_data['score21']
		score22 = self.cleaned_data['score22']
		score31 = self.cleaned_data['score31']
		score32 = self.cleaned_data['score32']
		score41 = self.cleaned_data['score41']
		score42 = self.cleaned_data['score42']
		score51 = self.cleaned_data['score51']
		score52 = self.cleaned_data['score52']

		set1_score = str(score11)+str(score12)
		set2_score = str(score21)+str(score22)
		set3_score = str(score31)+str(score32)
		set4_score = str(score41)+str(score42)
		set5_score = str(score51)+str(score52)
		finish_flag = False
		if set1_score in SET_SCORE:
			if score11 > score12:
				self.player1_set_point += 1
			else:
				self.player2_set_point += 1
		else:
			raise forms.ValidationError('第1局比分出错')

		if set2_score in SET_SCORE:
			if score21 > score22:
				self.player1_set_point += 1
			else:
				self.player2_set_point += 1
		else:
			raise forms.ValidationError('第2局比分出错')

		if set3_score in SET_SCORE:
			if score31 > score32:
				self.player1_set_point += 1
			else:
				self.player2_set_point += 1
			if self.player1_set_point == 3 or self.player2_set_point == 3:
				finish_flag = True
		elif set3_score == '00' or (score31 is None and score32 is None):
			finish_flag = True
			if self.player1_set_point == 1:
				raise forms.ValidationError('比赛不能为平局')
		else:
			raise forms.ValidationError('第3局比分出错')
		print 'after set 3 %s' % finish_flag

		if set4_score in SET_SCORE:
			if not finish_flag:
				if score41 > score42:
					self.player1_set_point += 1
				else:
					self.player2_set_point += 1
				if self.player1_set_point == 3 or self.player2_set_point == 3:
					finish_flag = True
			else:
				raise forms.ValidationError('不需要第4局比分了')
		elif (set4_score == '00' or (score41 is None and score42 is None)) and not finish_flag:
			finish_flag = True
			if (score11>score12 and score21>score22) or (score11<score12 and score21<score22):
				raise forms.ValidationError('请填写第5局比分')
		elif not finish_flag:
			raise forms.ValidationError('第4局比分出错')

		if set5_score in SET_SCORE:
			if not finish_flag:
				if score51 > score52:
					self.player1_set_point += 1
				else:
					self.player2_set_point += 1
			else:
				raise forms.ValidationError('不需要第5局比分')
		elif (set5_score == '00' or (score51 is None and score52 is None))and not finish_flag:
			raise forms.ValidationError('比赛不能为平局')
		elif not finish_flag:
			raise forms.ValidationError('第4局比分出错')

		return cleaned_data

	def save(self, commit=True):
		score = super(ScoreCreationForm,self).save(commit=False)
		score.set1 = self.player1_set_point
		score.set2 = self.player2_set_point
		if commit:
			score.save()
		return score

class GameGroupForm(forms.ModelForm):
	# holder = forms.CharField(widget=forms.TextInput(attrs = {'class': 'form-control'}))
	maximum = forms.IntegerField(min_value = 2, max_value = 8, widget=forms.NumberInput(attrs = {'class': 'form-control'}), initial=4, required=True)
	city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs = {'class': 'form-control'}), required=True)
	# district = forms.ModelChoiceField(queryset=District.objects.all(), widget=forms.Select(attrs = {'class': 'form-control'}))
	court = forms.ModelChoiceField(queryset=Court.objects.all().order_by('id').reverse(), widget=forms.Select(attrs = {'class': 'form-control'}), required=True)
	date = forms.DateField(input_formats=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%Y/%m/%d', '%Y %m %d', # '2006-10-25', '10/25/2006', '10/25/06'
		'%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
		'%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
		'%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
		'%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
		), widget=forms.widgets.DateInput(attrs = {'class': 'form-control','type':'date'}), initial=datetime.now(), required=True)
	start_time = forms.TimeField(widget=forms.widgets.TimeInput(format = '%H:%M', attrs = {'class': 'form-control','type':'time',}), initial=datetime.now(), required=True)
	last_hour = forms.IntegerField(min_value = 0, max_value = 12, widget=forms.NumberInput(attrs = {'class': 'form-control'}), initial=2, required=True)
	level_low = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=LEVEL, initial=2, required=True)
	level_high = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control'}),choices=LEVEL, initial=5.5, required=True)
	price = forms.IntegerField(min_value = 0, widget=forms.NumberInput(attrs = {'class': 'form-control'}), initial = 50, required=True)
	# gender = forms.ChoiceField(choices=GENDER, widget=forms.Select(attrs = {'class': 'form-control'}))
	description = forms.CharField(widget=forms.Textarea(attrs = {'class': 'form-control'}), initial = '欢迎加入我的小组!', required = True)

	class Meta:
		model = GameGroup
		fields = ('maximum', 'city', 'court', 'date', 'start_time', 'last_hour', 'level_low', 'level_high', 'price', 'description', )

	def clean_date(self):
		date = self.cleaned_data['date']
		if date < date.today():
			raise forms.ValidationError("时间已过，无法约球！")
		elif date > (date.today() + timedelta(days=60)):
			raise forms.ValidationError("您的约球时间太远了！")

		return date

	def clean(self):
		level_low = self.cleaned_data['level_low']
		level_high = self.cleaned_data['level_high']
		if level_low > level_high:
			raise forms.ValidationError("请正确填写等级范围！")
		return self.cleaned_data
