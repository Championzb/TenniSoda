from django import forms
from models import Profile
from localflavor.cn.forms import CNCellNumberField, CNProvinceSelect 

class UserProfileForm(forms.ModelForm):
	phone = CNCellNumberField ()
#	province = forms.CharField(max_length=50,widget=CNProvinceSelect)
	
	class Meta:
		model = Profile
		fields = ('username','level','gender','city')

	def save(self,commit=True):
		form = super(UserProfileForm,self).save(commit=False)
		form.phone = self.cleaned_data['phone']
#		form.province = self.cleaned_data['province']
		if commit:
			form.save()
		return form

	
