import random
import string

from django.shortcuts import render
from pymongo import MongoClient


# Drive Upload
def drive_upload(request):
    if request.method == 'POST' :
        try :
            con=MongoClient()
            db = con["tnp_management"]
            collection_student = db["registration_student"]
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

            query = {
                "tenth": {"$gte": request.POST.get('tenth')},
                "diploma_12": {"$gte": request.POST.get("diploma_12")},
                "marks": {"$gte": request.POST.get("engineering")},
                "branch": request.POST.get("branch"),
            }

            eligible_student = []
            student_details = collection_student.find(query)
            for i in student_details:
                print(i)
                id = i["_id"]
                name = i["name"]
                branch = i["branch"]
                student_temp = {"_id": id, "name": name, "branch": branch}
                eligible_student.append(student_temp)


            drive_dic={
                '_id': drive_id,
                'company_name' : request.POST.get("name"),
                'date': request.POST.get("drive_date"),
                'venue' : request.POST.get("place"),
                'time': request.POST.get("drive_time"),
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
                'eligible_student': eligible_student,
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


companyname = []
time = []

def student_attendence(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection = db["registration_student"]
            collect_drive = db["drive_drive"]

            query = {
                "_id": request.POST.get('pnr'),
                "primary_mobile": request.POST.get('primary_mobile'),
            }

            query1 = {
                "date": request.POST.get('drive_date'),
            }

            docs = collection.find(query)
            id = None
            name = None
            branch = None
            for i in docs:
                print(i)
                id = i['_id']
                name = i["name"]
                branch = i["branch"]

            doc = collect_drive.find(query1)
            companyname.clear()
            time.clear()
            for i in doc:
                companyname.append(i["company_name"])
                time.append(i["time"])

            return render(request, 'drive/student_list.html',
                          {"id": id, 'name': name, 'branch': branch, 'company_name': companyname, 'time': time})
        except Exception as e:
            print(e)
            return render(request, 'drive/student_attendance.html', {"error": 'Some error occured'})

    else:
        return render(request, 'drive/student_attendance.html', {})


def student_list(request):
    if request.method == 'POST':
        print("in")

        student_attendence_dict = {}
        for i in companyname:
            student_attendence_dict.update({i: request.POST.get(str(i))})

        try:
            student_list = {
                'id': request.POST.get('id'),
                'studen t_name': request.POST.get('name'),
                'branch': request.POST.get('branch'),
                'company_name': request.POST.get('company_name'),
                'drive_time': request.POST.get('time'),
                'status': request.POST.get('status')
            }
            print(student_list)
        except Exception as e:
            print(e)
            return render(request, 'drive/student_list.html', {"error": 'Some error occured'})
        return render(request, 'drive/driveupload.html', {})
    else:
        return render(request, 'drive/student_list.html', {})
