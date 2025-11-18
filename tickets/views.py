from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest , Reservation , Movie

# Create your views here.

# 1 => without REST and no model query Function Based View FBV
def no_rest_no_model(request):
    guest = [
        {
            'id' : 1 ,
            'name' : 'ahmed' ,
            'mobile' : '01156501103' ,
        },
        {
            'id' : 2 ,
            'name' : 'ali' ,
            'mobile' : '01287891103' ,
        }
    ]
    return JsonResponse(guest , safe= False)

# 2 => model data defult django whitout rest
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guists' : list( data.values('name' , 'mobile'))
    }
    return JsonResponse (response)


# list == GET 
# creat == POST
# pk query == GET 
# update == PUT 
# delete or destroy == DELETE 

# 3 => Function based views


