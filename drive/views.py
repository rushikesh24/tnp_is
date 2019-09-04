from django.shortcuts import render
from pymongo import MongoClient

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def drive_upload(request):
    if request.method == 'POST' :
        try :
            con=MongoClient()
            db = con["tnp_management"]
            collection = db["registration_drive"]

            drive_dic={
                'drive_id' : request.POST.get("Drive_id"),
                'company_name' : request.POST.get("name"),
                'date' : request.POST.get("drive_date"),
                'venue' : request.POST.get("place"),
                'time' : request.POST.get("drive_time"),
                'rounds' : request.POST.get("no_of_rounds"),
                'login_key' : request.POST.get("log_key"),
                'eligibility' : request.POST.get("eligible"),
                'base_package' : request.POST.get("package"),
                'campus_type' : request.POST.get("company_type"),
            }
            print(drive_dic)
            rec=collection.insert_one(drive_dic)
            print(rec)
            return  HttpResponse("Done Successfully")
        except Exception as e:
            return render(request, 'drive/driveupload.html', {"error": "Drive_id number is already registered"})
    else:
        return render(request, 'drive/driveupload.html', {})

