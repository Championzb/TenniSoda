#-*-coding:utf-8-*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from account.admin import UserCreationForm
from django.core.context_processors import csrf
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'您已经成功注册， 请去您的邮箱 %s 激活帐号！' % (form.cleaned_data['email']))
            return HttpResponseRedirect('/account/login/')
    else:
        form = UserCreationForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render_to_response('landing-index.html', args)
