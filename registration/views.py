from django.shortcuts import render
from pymongo import MongoClient

from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })


def single_student(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection = db["registration_student"]

            data_dic = {
                "_id": request.POST.get("pnr"),
                "name": request.POST.get("name"),
                "email": request.POST.get("email"),
                "tenth": request.POST.get("percentage"),
                "birthdate": request.POST.get("dob"),
                "diploma_12": request.POST.get("percentage1"),
                "placed" : request.POST.get("placed"),
                "branch": request.POST.get("branch"),
                "gender": request.POST.get("Gender"),
                "primary_mobile": request.POST.get("primary_mobile"),
                "secondary_mobile": request.POST.get("secondary_mobile"),
                "marks": request.POST.get("marks")
            }
            print(data_dic)
            rec = collection.insert_one(data_dic)
            print(rec)
            return HttpResponse("200")
        except Exception as e:
            return render(request, 'registration/student_single.html', {"error": "PNR number is already registered"})
    else:
        return render(request, 'registration/student_single.html', {})