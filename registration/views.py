from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from pymongo import MongoClient

from .forms import UserForm, UserProfileInfoForm


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
        collection = None
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection = db["registration_student"]
        except Exception as e:
            print(e)
            return render(request, 'registration/student_single.html', {"error": "Connection Failed"})

        if 'single' in request.POST:
            print("single")
            try:
                placed = request.POST.get("placed")
                if placed == None:
                    placed = False
                else:
                    placed = True
                data_dic = {
                    "_id": request.POST.get("pnr"),
                    "name": request.POST.get("name"),
                    "email": request.POST.get("email"),
                    "tenth": request.POST.get("percentage"),
                    "diploma_12": request.POST.get("percentage1"),
                    "birthdate" : request.POST.get("dob"),
                    "placed": placed,
                    "branch": request.POST.get("branch"),
                    "gender": request.POST.get("Gender"),
                    "primary_mobile": request.POST.get("primary_mobile"),
                    "secondary_mobile": request.POST.get("secondary_mobile"),
                    "marks": request.POST.get("marks"),
                }
                rec = collection.insert_one(data_dic)
                print(rec)

                return HttpResponse("200")
            except Exception as e:
                print(e)
                return render(request, 'registration/student_single.html',
                              {"error": "PNR number is already registered"})

        elif 'multiple' in request.POST:
            try:
                print('multiple')
                csv_file = request.FILES["csv_file"]
                if not csv_file.name.endswith('.csv'):
                    return HttpResponse('File is not CSV type')

                file_data = csv_file.read().decode("UTF-8")
                lines = file_data.split("\n")
                j = 0
                # loop over the lines and save them in db. If error , store as string and then display
                for line in lines:
                    fields = line.split(",")
                    data_dict = {}
                    data_dict["_id"] = fields[0]
                    data_dict["name"] = fields[1]
                    data_dict["email"] = fields[2]
                    data_dict["tenth"] = fields[3]
                    data_dict["diploma_12"] = fields[4]
                    data_dict["marks"] = fields[5]
                    data_dict["branch"] = fields[6]
                    data_dict["gender"] = fields[7]
                    if fields[8]:
                        data_dict["placed"] = True
                    else:
                        data_dict["placed"] = False
                    data_dict["primary_mobile"] = fields[9]
                    data_dict["secondary_mobile"] = fields[10]
                    j = j + 1
                    print(j)
                    rec = collection.insert_one(data_dict)
                return HttpResponse("Data Uploaded Successfully")
            except Exception as e:
                print(e)
                return HttpResponse("Unable to upload the file")
    else:
        return render(request, 'registration/student_single.html', {})

def employee(request):
    return render(request, 'registration/signup.html', {})
