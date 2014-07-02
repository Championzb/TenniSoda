from django.shortcuts import render_to_response
from models import District

# Create your views here.
'''
def get_district(request):
    if request.method == "POST":
        city = request.POST['city']
    else:
        city = ''

    district = District.objects.filter(city = city)

    return render_to_response('page-settings.html',{'district':district})
'''