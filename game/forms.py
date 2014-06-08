from django import forms
from models import Score

class ScoreCreationForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ('score11','score12','score21','score22','score31','score32','score41','score42','score51','score52')
