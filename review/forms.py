from django import forms
from models import CourtReview, RateReview

RATE=(('1','Terrible'),('2','Bad'),('3','Fair'),('4','Good'),('5','Excellent'),)

class CourtReviewCreationForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs = {'class': 'form-control parsley-validated'}), required=False)
    rate = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control parsley-validated'}),choices=RATE,required=False)
    class Meta:
        model = CourtReview
        fields = ('review','rate',)


class RateReviewCreationForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs = {'class': 'form-control parsley-validated'}), required=False)
    rate = forms.ChoiceField(widget=forms.Select(attrs = {'class': 'form-control parsley-validated'}),choices=RATE,required=False)

    class Meta:
        model = RateReview
        fields = ('review','rate',)