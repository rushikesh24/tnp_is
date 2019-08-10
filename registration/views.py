from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,HttpResponse

# Create your views here.
from pymongo.auth import authenticate


def registration(request):
    if request.method == 'POST':
        print("Hello")
        form = UserCreationForm(request.POST)
        username = request.POST.get('username')
        raw_password = request.POST.get('id_password1')
        print(str(username)+str(raw_password))
        #user = authenticate(username=username, password=raw_password)
        #login(request, user)
        return HttpResponse(username + raw_password)
    else:
        print('Hello World...')
    return render(request,'registration.html',{})