from django import forms
from models import Score, Game
from django.forms import extras

SET_SCORE = ('60','61','62','63','64','75','57','76','67','06','16','26','36','46',)
class GameEditForm(forms.ModelForm):
    date = forms.DateField(widget=extras.SelectDateWidget(years=range(2014,2015)))

    class Meta:
        model = Game
        fields = ('court', 'date')

class ScoreCreationForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ('score11','score12','score21','score22','score31','score32','score41','score42','score51','score52')


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
        player1_set_point = 0
        player2_set_point = 0
        finish_flag = False
        if set1_score in SET_SCORE:
            if score11 > score12:
                player1_set_point += 1
            else:
                player2_set_point += 1
        else:
            raise forms.ValidationError('set 1 invalid set score')

        if set2_score in SET_SCORE:
            if score21 > score22:
                player1_set_point += 1
            else:
                player2_set_point += 1
        else:
            raise forms.ValidationError('set 2 invalid set score')

        if set3_score in SET_SCORE:
            if score31 > score32:
                player1_set_point += 1
            else:
                player2_set_point += 1
            if player1_set_point == 3 or player2_set_point == 3:
                print 'in set 3 score %s %s' % (player1_set_point,player2_set_point)
                print 'in set 3 %s' % finish_flag
                finish_flag = True
        elif set3_score == '00' or (score31 is None and score32 is None):
            finish_flag = True
            if player1_set_point == 1:
                raise forms.ValidationError('can not be draw')
        else:
            raise forms.ValidationError('set 3 invalid set score')
        print 'after set 3 %s' % finish_flag

        if set4_score in SET_SCORE:
            if not finish_flag:
                if score41 > score42:
                    player1_set_point += 1
                else:
                    player2_set_point += 1
                if player1_set_point == 3 or player2_set_point == 3:
                    finish_flag = True
            else:
                raise forms.ValidationError('set 4 is not necessary')
        elif (set4_score == '00' or (score41 is None and score42 is None)) and not finish_flag:
            finish_flag = True
            if (score11>score12 and score21>score22) or (score11<score12 and score21<score22):
                raise forms.ValidationError('set 3 is not neccessary or game is in 5 sets')
        elif not finish_flag:
            raise forms.ValidationError('set 4 invalid set score')

        if set5_score in SET_SCORE:
            if not finish_flag:
                if score51 > score52:
                    player1_set_point += 1
                else:
                    player2_set_point += 1
            else:
                raise forms.ValidationError('set 5 is not necessary')
        elif (set5_score == '00' or (score51 is None and score52 is None))and not finish_flag:
            raise forms.ValidationError('can not be draw')
        elif not finish_flag:
            raise forms.ValidationError('set 4 invalid set score')

        return cleaned_data
