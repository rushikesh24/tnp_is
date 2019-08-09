from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
from pymongo.auth import authenticate


def registration(request):
    if request.method == 'POST':
        print("Hello")
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('id_password1')
            #print(str(username)+str(raw_password))
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        print('Hello World...')
        form = UserCreationForm()
    return render(request,'registration.html',{})