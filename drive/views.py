import random
import string

from django.shortcuts import render
from pymongo import MongoClient


def drive_upload(request):
    if request.method == 'POST' :
        try :
            con=MongoClient()
            db = con["tnp_management"]
            collection = db["drive_drive"]

            date_ls = str(request.POST.get("drive_date")).split("-")
            drive_id = str(request.POST.get("name")) + str(date_ls[0])
            login_key = randomStringDigits()

            round_ls = str(request.POST.get("other")).split(',')
            round_dict = {}
            j = 0
            for i in round_ls:
                j = j + 1
                round_name = "round_" + str(j)
                round_dict.update({round_name: i})

            drive_dic={
                '_id': drive_id,
                'company_name' : request.POST.get("name"),
                # 'date' : request.POST.get("drive_date"),
                'venue' : request.POST.get("place"),
                # 'time' : request.POST.get("drive_time"),
                'rounds': round_dict,
                'login_key': login_key,
                'branch': request.POST.get("branch"),
                'eligibility': {
                    'tenth_marks': request.POST.get("tenth"),
                    'diploma_12': request.POST.get("diploma_12"),
                    'engg': request.POST.get("engineering"),
                },
                'base_package' : request.POST.get("package"),
                'campus_type': request.POST.get("campus"),
            }
            rec=collection.insert_one(drive_dic)
            print(rec)
            return render(request, 'drive/round_details.html', {
                'login_key': login_key,

            })
        except Exception as e:
            print(e)
            return render(request, 'drive/driveupload.html', {"error": "Drive_id number is already registered"})
    else:
        return render(request, 'drive/driveupload.html', {})


def randomStringDigits(stringLength=8):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


def student_attendence(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection = db["registration_student"]

            query = {
                "_id": request.POST.get('pnr'),
                "primary_mobile": request.POST.get('primary_mobile'),
            }

            docs = collection.find(query)
            for i in docs:
                id = i['_id']
                name = i["name"]
            return render(request, 'drive/student_list.html', {"id": id, 'name': name})
        except Exception as e:
            print(e)
            return render(request, 'drive/student_attendance.html', {"error": 'Some error occured'})

    else:
        return render(request, 'drive/student_attendance.html', {})
