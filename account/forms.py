from django import forms
from models import Profile
from court.models import Court
from localflavor.cn.forms import CNCellNumberField, CNProvinceSelect 

LEVEL=(('1','1(low)'),('1.5','1.5'),('2','2'),('2.5','2.5'),('3','3'),('3.5','3.5'),('4','4(median)'),('4.5','4.5'),('5','5'),('5.5','5.5'),('6','6'),('6.5','6.5'),('7','7'),('7.5','7.5(high)'),)
GENDER=(('1','male'),('0','female'))
CITY=(('1','Suzhou'),('2','Beijing'),('3','Shanghai'))

class UserProfileForm(forms.ModelForm):
	level = forms.ChoiceField(widget=forms.Select(),choices=LEVEL)
	gender = forms.ChoiceField(widget=forms.Select(),choices=GENDER)
	city = forms.ChoiceField(widget=forms.Select(),choices=CITY)
	phone = CNCellNumberField ()
	court = forms.ChoiceField(widget=forms.Select(),choices=Court.objects.all())


	class Meta:
		model = Profile
		fields = ('first_name','last_name','birth_date','court','level','gender','city')

	def save(self,commit=True):
		form = super(UserProfileForm,self).save(commit=False)
		form.phone = self.cleaned_data['phone']
		if commit:
			form.save()
		return form

	
