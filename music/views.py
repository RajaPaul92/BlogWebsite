from django.http import HttpResponse
from rest_framework.views import APIView
from pymongo import MongoClient, CursorType
from django.shortcuts import render
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import requests
from bson import ObjectId

client = MongoClient('mongodb://test1234:test1234@206.189.23.214:27017/pythontest', connect=False)
db = client.pythontest

def index(request):
    return render(request, 'website/login.html')


def empDetails(request):
    empData = requests.get('http://127.0.0.1:8000/empDetailsAPI/')
    print(empData)
    data = []
    empData_json = empData.json()
    for i in empData_json['result']:
        data.append({
            'id': str(i['id']),
            'name': i['name'],
            'email': i['email'],
            'password': i['password'],
            'phone': i['phone'],
            'status': i['status'],
            'statusMsg': i['statusMsg']
        })
    print (data)
    return render(request, 'website/empDetails.html', context={"data": data})


class empDetailsAPI(APIView):
    def get(self,request):
        dataDB= db.blogUser.find({'status':1})
        finalData= []
        for i in dataDB:
            finalData.append({
                'id': str(i['_id']),
                'name': i['name'],
                'email': i['email'],
                'password': i['password'],
                'phone': i['phone'],
                'status': i['status'],
                'statusMsg': i['statusMsg']
            })
        response_message= {
            "message":"successful",
            "result":finalData
        }
        return JsonResponse(response_message, safe= False, status= 200)


def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    get_data = {
        "email": email,
        "password": password
    }
    print (get_data)
    my_data = requests.post('http://127.0.0.1:8000/loginAPI/', json=get_data)
    my_data_json = my_data.json()
    if (my_data.status_code == 200):
        user_id = my_data_json['data']
        print(user_id)
        request.session['user_id'] = user_id
        return render(request,'website/index.html')
    else:
        return HttpResponse("invalid login password")




class loginAPI(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        data = db.blogAdmin.find({'email': email, 'password': password})
        print (data)
        for i in data:
            print (i)
            id = str(i['_id'])
            print (id)
        if data.count() > 0:
            response_message = {
                "message": "successfully logged in",
                "data":id
            }
            return JsonResponse(response_message, safe=False, status=200)

        else:
            response_message = {
                "message": "invalid login or password"
            }
            return JsonResponse(response_message, safe=False, status=302)


def empAdd(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    phone = request.POST.get('phone')
    get_data = {
        "name": name,
        "email": email,
        "password": password,
        "phone": phone
    }
    print (get_data)
    mydata = requests.post('http://127.0.0.1:8000/empAddAPI/', json=get_data)
    if (mydata.status_code == 200):
        return redirect('/empDetails/')
    else:
        return HttpResponse("incorrect input")


class empAddAPI(APIView):
    def post(self, request):
        name = request.data['name']
        email = request.data['email']
        password = request.data['password']
        phone = request.data['phone']
        checkData= db.blogUser.find({'email': email}).count()
        if checkData > 0:
            print ("email already exist")
            response_message= {
                "message" : "email already exist",
                "data": []
            }
            return JsonResponse(response_message, safe= False, status = 302)
        else:
            data = {
                'name': name,
                'email': email,
                'password': password,
                'phone': phone,
                'status': 1,
                'statusMsg': 'Active'
            }
            print (data)
            db.blogUser.insert(data)
            response_message= {
                "message" : "successfully inserted",
                "data": []
            }
            return JsonResponse(response_message, safe= False, status = 200)

def editEmployee(request, id):
    get_data = db.blogUser.find({'_id': ObjectId(id)})
    print (get_data)
    for i in get_data:
        id = str(i['_id'])
        name = i['name']
        email = i['email']
        password = i['password']
        phone = i['phone']
    return render(request,'website/updateEmp.html', context={'id':id, 'name':name, 'email':email, 'password':password, 'phone':phone})

def updateEmp(request, id):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    phone = request.POST.get('phone')
    updateData= {
        "name":name,
        "email":email,
        "password":password,
        "phone":phone
    }
    print (updateData)
    empData = requests.patch('http://127.0.0.1:8000/updateEmpAPI/'+id+'/',json=updateData)
    if(empData.status_code == 200):
        return redirect('/empDetails/')
    else:
        return redirect(request,'website/updateEmp.html')



class updateEmpAPI(APIView):
    def patch(self,request,id):
        name = request.data['name']
        email = request.data['email']
        password = request.data['password']
        phone = request.data['phone']
        data=db.blogUser.update({'_id':ObjectId(id)}, {'$set':{'name':name, 'email':email, 'password':password, 'phone':phone}})
        response_message = {
            "message": "Successfully updated",
            "data": []
        }
        print (data)
        return JsonResponse(response_message, safe=False, status=200)

def deleteEmployee(request,id):
    db.blogUser.update_one({
        '_id': ObjectId(id)
    }, {
        '$set': {'status': 2, 'statusMsg': 'Inactive'}
    }, upsert=False)

    return redirect('/empDetails/')


def blog(request):
    blogdata = requests.get('http://127.0.0.1:8000/blogAPI/')
    print (blogdata)
    data = []
    data_json = blogdata.json()
    for i in data_json['result']:
        data.append({
            'id': str(i['id']),
            'title': i['title'],
            'description': i['description'],
            'statusmsg': i['statusmsg']
        })
    print (data)
    return render(request,'website/blog.html', context={'data':data})

class blogAPI(APIView):
    def get(self,request):
        get_data = db.blog.find({'status':1})
        finalData= []
        for i in get_data:
            finalData.append({
                'id':str(i['_id']),
                'title':i['title'],
                'description': i['description'],
                'statusmsg': i['statusmsg']
            })
        response_message = {
            "message": "successful",
            "result": finalData
        }
        return JsonResponse(response_message, safe=False, status=200)

def blogDetails(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    data = {
        'title': title,
        'description': description
    }
    print (data)
    mydata = requests.post('http://127.0.0.1:8000/blogDetailsAPI/', json=data)
    if(mydata.status_code == 200):
        return redirect('/blog/')
    else:
        return HttpResponse('invalid data')

class blogDetailsAPI(APIView):
    def post(self, request):
        title = request.data['title']
        description = request.data['description']
        getData ={
            'title': title,
            'description': description,
            'status':1,
            'statusmsg': "Active"
        }
        db.blog.insert(getData)
        response_message = {
            'message': "succuessfully inserted",
            'data': []
        }
        return JsonResponse(response_message, safe= False, status=200)

def editblog(request,id):
    getdata = db.blog.find({'_id': ObjectId(id)})
    print (getdata)
    for i in getdata:
        id = str(i['_id'])
        title = i['title']
        description = i['description']
    return render(request, 'website/editblog.html', context={'id': id, 'title': title, 'description':description})

def updateblog(request, id):
    title = request.POST.get('title')
    description = request.POST.get('description')
    updateData = {
        'title': title,
        'description': description
    }
    print (updateData)
    my_data = requests.patch('http://127.0.0.1:8000/updateblogAPI/'+id+'/', json = updateData)
    if(my_data.status_code == 200):
        return redirect('/blog/')
    else:
        return render(request, 'website/editblog.html')

class updateblogAPI(APIView):
    def patch(self, request,id):
        title= request.data['title']
        description = request.data['description']
        data = db.blog.update({'_id': ObjectId(id)}, {'$set': {'title': title, 'description': description}})
        print (data)
        response_message= {
            "message": "successfully updated",
            "data": []
        }
        return JsonResponse(response_message, safe = False, status=200)

def deleteblog(request, id):
    db.blog.update_one({
        '_id': ObjectId(id)
    }, {
        '$set': {'status': 2, 'statusMsg': 'Inactive'}
    }, upsert=False)

    return redirect('/blog/')


def userlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    userData = {
        'email': email,
        'password': password
    }
    print (userData)
    mydata = requests.post('http://127.0.0.1:8000/userloginAPI/', json=userData)
    my_data_json = mydata.json()
    user_id = my_data_json['data']
    if(mydata.status_code == 200):
        request.session['user_id'] = user_id
        return redirect('/userdata/')
    else:
        return HttpResponse("invalid user login password")



class userloginAPI(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        getData = db.blogUser.find({'email': email, 'password': password})
        print (getData)
        for i in getData:
            print (i)
            id = str(i['_id'])
        if getData.count() > 0:
            response_message= {
                'message': "successfully logged in",
                "data": id
            }
            return JsonResponse(response_message,safe = False, status=200)
        else:
            response_message = {
                "message": "invalid login",
            }
            return JsonResponse(response_message, safe= False, status= 302)


def userdata(request):
    user_id = str(request.session.get('user_id'))
    print (user_id)
    header = {"userId": user_id}
    id_status = db.blogUser.find({'_id': ObjectId(user_id), 'status': 1})
    if id_status.count() > 0:
        for i in id_status:
            print (i)
            name = i['name']
        my_data = requests.get('http://127.0.0.1:8000/userdataAPI/', headers=header)
        data = []
        my_data_json = my_data.json()
        for i in my_data_json['result']:
            print (i)
            data.append({
                "id": str(i['id']),
                "user_id": i['user_id'],
                "title": i['title'],
                "description": i['description'],
                # "statusmsg": i['statusMsg']
            })
        print(data)
        return render(request, 'website/userblog.html', context={"data": data, "name": name})
    else:
        return render(request, 'website/login.html')

class userdataAPI(APIView):
    def get(self,request):
        user_id = request.META['HTTP_USERID']
        dataDB = db.blog.find({'status': 1, 'user_id': user_id})
        finalData = []
        for i in dataDB:
            finalData.append({
                'id': str(i['_id']),
                'user_id': i['user_id'],
                'title': i['title'],
                'description': i['description']
            })
        response_message = {
            "message": "Successful",
            "result": finalData
        }
        return JsonResponse(response_message, safe=False, status=200)

def userblogDetails(request):
    user_id = str(request.session.get('user_id'))
    print (user_id)
    id_status = db.blogUser.find({'_id': ObjectId(user_id), 'status': 1})
    print (id_status)
    if id_status.count() > 0:
        title = request.POST.get('title')
        description = request.POST.get('description')
        store_data = {
            "user_id": user_id,
            "title": title,
            "description": description
        }
        print (store_data)
        my_data = requests.post('http://127.0.0.1:8000/userblogDetailsAPI/', json=store_data)
        if (my_data.status_code == 200):
            return redirect('/userdata/')
        else:
            return render(request, 'website/userblog.html')
    else:
        return render(request,'website/userblog.html')

class userblogDetailsAPI(APIView):
    def post(self, request):
        user_id = request.data['user_id']
        print (user_id)
        title = request.data['title']
        description = request.data['description']
        get_data = db.blog.insert({ "user_id": user_id,"title":title, "description": description, "status": 1, "statusmsg": "Active"})
        print(get_data)
        response_message = {
            "message": "Successfully",
            "data": []
        }
        return JsonResponse(response_message, safe=False, status=200)

def usereditblog(request,id):
    getdata = db.blog.find({'_id': ObjectId(id)})
    print (getdata)
    for i in getdata:
        id = str(i['_id'])
        title = i['title']
        description = i['description']
    return render(request, 'website/updateUser.html', context={'id': id, 'title': title, 'description':description})

def userupdateblog(request, id):
    title = request.POST.get('title')
    description = request.POST.get('description')
    updateData = {
        'title': title,
        'description': description
    }
    print (updateData)
    my_data = requests.patch('http://127.0.0.1:8000/updateblogAPI/'+id+'/', json = updateData)
    if(my_data.status_code == 200):
        return redirect('/userdata/')
    else:
        return render(request, 'website/userblog.html')

class userupdateblogAPI(APIView):
    def patch(self, request,id):
        title= request.data['title']
        description = request.data['description']
        data = db.blog.update({'_id': ObjectId(id)}, {'$set': {'title': title, 'description': description}})
        print (data)
        response_message= {
            "message": "successfully updated",
            "data": []
        }
        return JsonResponse(response_message, safe = False, status=200)

def userdeleteblog(request, id):
    db.blog.update_one({
        '_id': ObjectId(id)
    }, {
        '$set': {'status': 2, 'statusmsg': 'Inactive'}
    }, upsert=False)

    return redirect('/userdata/')



def comment(request):
    blogdata = requests.get('http://127.0.0.1:8000/commentAPI/')
    print (blogdata)
    data = []
    data_json = blogdata.json()
    for i in data_json['result']:
        data.append({
            'id': str(i['id']),
            'title': i['title'],
            'description': i['description'],
            'comment': i['comment'],
            'statusmsg': i['statusmsg']
        })
    print (data)
    return render(request,'website/comment.html', context={'data':data})

class commentAPI(APIView):
    def get(self,request):
        get_data = db.comment.find({'status':1})
        finalData= []
        for i in get_data:
            finalData.append({
                'id':str(i['_id']),
                'title':i['title'],
                'description': i['description'],
                'comment': i['comment'],
                'statusmsg': i['statusmsg']
            })
        response_message = {
            "message": "successful",
            "result": finalData
        }
        return JsonResponse(response_message, safe=False, status=200)

def commentDetails(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    comment= request.POST.get('comment')
    data = {
        'title': title,
        'description': description,
        'comment': comment
    }
    print (data)
    mydata = requests.post('http://127.0.0.1:8000/commentDetailsAPI/', json=data)
    if(mydata.status_code == 200):
        return redirect('/comment/')
    else:
        return HttpResponse('invalid data')

class commentDetailsAPI(APIView):
    def post(self, request):
        title = request.data['title']
        description = request.data['description']
        comment = request.data['comment']
        getData ={
            'title': title,
            'description': description,
            'comment': comment,
            'status':1,
            'statusmsg': "Active"
        }
        db.comment.insert(getData)
        response_message = {
            'message': "succuessfully inserted",
            'data': []
        }
        return JsonResponse(response_message, safe= False, status=200)
