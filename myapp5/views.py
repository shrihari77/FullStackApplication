from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import json
from .models import register
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def reg(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        fname = data.get('fname')
        lname = data.get('lname')
        phone = data.get('phone') 
        email = data.get('email')
        password = data.get('password')

        register.objects.create(
            fname=fname,
            lname=lname,
            phone=phone,
            email=email,
            password=password
        ) 
        return JsonResponse({"message":"Registered Sucessfull"}, status=201)
    return JsonResponse({"Error": "POST method only"}, status=405)

@csrf_exempt

def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')

        
        user = register.objects.get(email=email, password=password)
        if user:
            return JsonResponse({"message": "Login Successful"})
        else:
            
            return JsonResponse({"Error": "Invalid email or password"})
    return JsonResponse({"Error": "POST method only"})

@csrf_exempt
def get_data(request):
    if request.method == 'GET':
        data = register.objects.all()
        sample = []
        for users in data:
            sample.append({
                "id": users.id,
                "fname": users.fname,
                "lname": users.lname,
                "phone": users.phone,
                "email": users.email,
                "password": users.password
            })
        return JsonResponse({"details": sample}, safe=False)
    else:
        return JsonResponse({"Error": "GET method only"})

    
@csrf_exempt
def delete_data(request):
    if request.method == 'DELETE':
        data = json.loads(request.body.decode('utf-8'))
        Id = data.get('id')
        remove = register.objects.filter(id=Id)
        if remove.exists():
            remove.delete()
            return JsonResponse({"message": "Deleted successfully"})
        else:
            return JsonResponse({"message": "Deleted unsuccessfully"})
    return JsonResponse({"Error": "DELETE method only"})
    
@csrf_exempt
def update_data(request):
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        Id = data.get('id')
        
        if not register.objects.filter(id=Id).exists():
            return JsonResponse({"message": "User not found"})
        
        register.objects.filter(id=Id).update(
        fname = data.get('fname'),
        lname = data.get('lname'),
        phone = data.get('phone'),
        email = data.get('email'),
        password = data.get('password')
        )
        return JsonResponse({"message": "Updated successfully"})
    return JsonResponse({"Error": "PUT method only"})
        