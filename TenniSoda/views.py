from django.shortcuts import render_to_response
from account.admin import UserCreationForm
from django.core.context_processors import csrf

def home(request):
    if request == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('account-login.html')
    else:
        form = UserCreationForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render_to_response('landing-index.html', args)