from django.contrib import admin
from models import CourtReview,RateReview
# Register your models here.

class CourtReviewAdmin(admin.ModelAdmin):
    list_display = ['game','court','player','reviewed_time', 'review']
    ordering = ['reviewed_time', ]
    search_fields = ('review', )

class RateReviewAdmin(admin.ModelAdmin):
    list_display = ['game','player','reviewed_time', 'review']
    ordering = ['reviewed_time', ]
    search_fields = ('review', )

admin.site.register(CourtReview,CourtReviewAdmin)
admin.site.register(RateReview,RateReviewAdmin)
