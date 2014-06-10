from django.contrib import admin
from models import CourtReview,RateReview
# Register your models here.

class CourtReviewAdmin(admin.ModelAdmin):
    list_display = ['game','court','player','reviewed_time']

class RateReviewAdmin(admin.ModelAdmin):
    list_display = ['game','player','reviewed_time']

admin.site.register(CourtReview,CourtReviewAdmin)
admin.site.register(RateReview,RateReviewAdmin)
