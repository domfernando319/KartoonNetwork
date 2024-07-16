from django.shortcuts import render
from account.models import User
from django.http import HttpResponse
# Create your views here.

def activateaccount(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    if email and id:
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
    
        return HttpResponse('Activation successful! Sign in!')
    else:
        return HttpResponse('The paramaters are invalid.')