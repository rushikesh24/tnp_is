from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient

''' For Date
def drive_upload(request):
    if request.method == 'POST' :
        # if this is a POST request we need to process the form data
        # create a form instance and populate it with data from the request:
        form = DriveDataForm(request.POST)
            # check whether it's valid:
        if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
            print(form.data['date'])
            collection = None
            try:
                con = MongoClient()
                db = con["tnp_management"]
                collection = db["drive_Drive"]
            except Exception as e:
                print(e)
                return render(request, 'registration/student_single.html', {"error": "Connection Failed"})

            try:
                data_dic = {
                    "date": form.data['date'],
                }
                rec = collection.insert_one(data_dic)
                print(rec)
            except Exception as e:
                print(e)
                return render(request, 'registration/student_single.html',
                              {"error": "PNR number is already registered"})

            return HttpResponseRedirect('thanks')
        # if a GET (or any other method) we'll create a blank form
        else:
            form = DriveDataForm()
    else:
        form = DriveDataForm()
    return render(request, 'drive/drive_upload.html', {'form': form})

'''
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
