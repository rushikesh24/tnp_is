import csv

import pymongo
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
    print("Logged OUt")
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Employee Registration
def employee_registeration(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        # print('rushi',profile_form.designation)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.username = user
            profile.save()
            print("profile saved successfully")  # Console log
            return render(request, 'home.html', {})
        else:
            print(user_form.errors, profile_form.errors)
            error = "user already registered"
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        error = ""
    return render(request, 'registration/employee_signup.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'error' : error
        })


# Candidate_upload
@login_required
def candidate_upload(request):
    if request.method == 'POST':
        collection = None
        try:
            #Create connection between database and user
            con = MongoClient()
            db = con["tnp_management"]
            collection = db["registration_candidate"]

            print("Connection established successfully")  #Console log
        except Exception as e:
            print(e)  # Console log
            return render(request, 'registration/candidate_upload.html', {"error": "Connection Failed"})

        #For single student
        if 'single' in request.POST:
            print("single student data upload")
            try:
                # To handle None values
                live_backlog = request.POST.get("live_backlog")
                if live_backlog == None:
                    live_backlog = False
                else:
                    live_backlog = True

                data_dic = {
                    "_id": request.POST.get("pnr"),
                    "name": request.POST.get("name"),
                    "gender": request.POST.get("Gender"),
                    "aadhar_number": request.POST.get("aadhaarcard"),
                    "email": request.POST.get("email"),
                    "primary_mobile": request.POST.get("primary_mobile"),
                    "secondary_mobile": request.POST.get("secondary_mobile"),
                    "tenth": request.POST.get("percentage"),
                    "diploma_12": request.POST.get("percentage1"),
                    "engineering": request.POST.get("marks"),
                    "college_name": request.POST.get("clgname"),
                    "branch": request.POST.get("branch"),
                    "live_backlog": live_backlog,
                    "placed": request.POST.get("placed"),
                    "eligible" : request.POST.get("placed"),
                    "round1" : request.POST.get("placed"),
                    "round2" : request.POST.get("placed"),
                    "round3" : request.POST.get("placed"),
                    "round4" : request.POST.get("placed"),
                    "round5" : request.POST.get("placed"),
                    "round6" : request.POST.get("placed"),
                    "round7" : request.POST.get("placed"),
                    "round8" : request.POST.get("placed"),
                }
                rec = collection.insert_one(data_dic)
                print("inserted_record")
                print(rec)
                return HttpResponse("candidate Uploaded Successfully")

            except Exception as e:
                print({"exeption": e})
                return render(request, 'registration/candidate_upload.html',
                              {"error": "PNR number is already registered"})

        elif 'multiple' in request.POST:
            error_data= []
            try:
                print("multiple student data upload")
                csv_file = request.FILES["csv_file"]
                if not csv_file.name.endswith('.csv'):
                    return HttpResponse('File is not CSV type. Please upload csv file')

                file_data = csv_file.read().decode("UTF-8")
                lines = file_data.split("\n")
                # loop over the lines and save them in db. If error , store as string and then display
                for line in lines:
                    try:
                        if line == '':
                            continue
                        fields = line.split(",")
                        data_dict = {}
                        data_dict["_id"] = fields[0]
                        data_dict["name"] = fields[1]
                        data_dict["gender"] = fields[2]
                        data_dict["aadhar_number"] = fields[3]
                        data_dict["email"] = fields[4]
                        data_dict["primary_mobile"] = fields[5]
                        data_dict["secondary_mobile"] = fields[6]
                        data_dict["tenth"] = fields[7]
                        data_dict["diploma_12"] = fields[8]
                        data_dict["college_name"] = fields[9]
                        if fields[10] == "Computer Engineering":
                            fields[10] = "computer"
                        elif fields[10] == 'Information Engineering':
                            fields[10] = 'information technology'
                        elif fields[10] == 'E&TC Engineering':
                            fields[10] = 'entc'
                        elif fields[10] == "Production Engineering":
                            fields[10] = "production"
                        elif fields[10] == 'Instrumentation Engineering':
                            fields[10] = 'instrumentation'
                        elif fields[10] == 'Civil Engineering':
                            fields[10] = 'civil'
                        elif fields[10] == 'Mechanical Engineering':
                            fields[10] = 'mechanical'
                        data_dict["branch"] = fields[10]
                        data_dict["engineering"] = fields[11]
                        if fields[12]:
                            data_dict["live_backlog"] = True
                        else:
                            data_dict["live_backlog"] = False
                        data_dict["placed"] = fields[13]
                        data_dict["eligible"] = fields[13]
                        data_dict["round1"] = fields[13]
                        data_dict["round2"] = fields[13]
                        data_dict["round3"] = fields[13]
                        data_dict["round4"] = fields[13]
                        data_dict["round5"] = fields[13]
                        data_dict["round6"] = fields[13]
                        data_dict["round7"] = fields[13]
                        data_dict["round8"] = fields[13]
                        rec = collection.insert_one(data_dict)
                        print("inserted_record")
                        print(rec)
                    except pymongo.errors.DuplicateKeyError as ex:
                        data_list = []
                        data_list.append(fields[0])
                        data_list.append(fields[1])
                        data_list.append(fields[2])
                        data_list.append(fields[3])
                        data_list.append(fields[4])
                        data_list.append(fields[5])
                        data_list.append(fields[6])
                        data_list.append(fields[7])
                        data_list.append(fields[8])
                        data_list.append(fields[9])
                        if fields[10] == "Computer Engineering":
                            fields[10] = "computer"
                        elif fields[10] == 'Information Engineering':
                            fields[10] = 'information technology'
                        elif fields[10] == 'E&TC Engineering':
                            fields[10] = 'entc'
                        elif fields[10] == "Production Engineering":
                            fields[10] = "production"
                        elif fields[10] == 'Instrumentation Engineering':
                            fields[10] = 'instrumentation'
                        elif fields[10] == 'Civil Engineering':
                            fields[10] = 'civil'
                        elif fields[10] == 'Mechanical Engineering':
                            fields[10] = 'mechanical'
                        data_list.append(fields[10])
                        data_list.append(fields[11])
                        if fields[12]:
                            data_list.append(True)
                        else:
                            data_list.append(False)
                        data_list.append(fields[13])
                        data_list.append(fields[13])
                        data_list.append(fields[13])
                        data_list.append(fields[13])
                        data_list.append(fields[13])
                        data_list.append(fields[13])
                        data_list.append(fields[13])
                        data_list.append(fields[13])
                        data_list.append(fields[13])
                        data_list.append(fields[13])
                        error_data.append(data_list)
                with open('other_files/Duplicate Record.csv', 'w') as f:
                    writer = csv.writer(f)
                    for row in error_data:
                        writer.writerow(row)
                f.close()
                return HttpResponse("Candidate Uploaded Successfully. <br>Duplicate PRN stored in Duplicate Record.csv.<br> No. of Duplicate records are "+str(len(error_data)))
            except Exception as e:
                print("exception",e,type(e))
                return HttpResponse("Unable to upload the file. Error in file"+str(e))

    else:
        return render(request, 'registration/candidate_upload.html', {})
