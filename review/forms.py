from django import forms
from models import CourtReview, RateReview

class CourtReviewCreationForm(forms.ModelForm):

    class Meta:
        model = CourtReview
        fields = ('review','rate',)


class RateReviewCreationForm(forms.ModelForm):

    class Meta:
        model = RateReview
        fields = ('review','rate',)