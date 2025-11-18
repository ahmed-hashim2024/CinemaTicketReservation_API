from django.shortcuts import render
from django.http.response import JsonResponse 
from .models import Guest , Reservation , Movie
from rest_framework.decorators import api_view
from .serializers import GuestSerializers
from rest_framework.response import Response
from rest_framework import status , filters 
from rest_framework.views import APIView
from django.http import Http404



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


# 3 => Function based views rest_framework
# 3.1 => GET , POST
@api_view( [ 'GET' , 'POST' ] )
def FBV_List ( request ) :

    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializers ( guests , many=True )
        return Response( serializer.data , status=status.HTTP_200_OK)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializers ( data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data , status = status.HTTP_201_CREATED)
        return Response( serializer.data , status = status.HTTP_400_BAD_REQUEST)


# 3.1 => GET , PUT , DELETE
@api_view(['GET' , 'PUt' , 'DELETE'])
def FBV_pk( request , pk):
    try:
        # 1. تحديد الكائن باستخدام الـ ID (pk)
        guest = Guest.objects.get(pk= pk)
    except Guest.DoesNotExist:
        # 2. إذا لم يتم العثور على الكائن
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET
    if request.method == 'GET':
        serializer = GuestSerializers ( guest )
        return Response( serializer.data )
    
    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializers ( data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data , status = status.HTTP_202_ACCEPTED)
        return Response( serializer.errors , status = status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    elif request.method == 'DELETE':
        guest.delete()
        return Response(  status = status.HTTP_204_NO_CONTENT)


# 4 => Class based views rest_framework
# 4.1 => list ,create ==> GET , POST
class CBV_list(APIView):
    def get(self , request):
        guests = Guest.objects.all()
        serializer = GuestSerializers(guests , many = True)
        return Response( serializer.data , status=status.HTTP_200_OK)
    
    def post(self , request):
        serializer = GuestSerializers (data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else :
            return Response (serializer.data , status = status.HTTP_400_BAD_REQUEST )


# 4.2 => pk_query , update , DELETE ==> GET , PUT , DELETE
class CBV_pk(APIView):
    def get_object( self , pk ):
        try:
            return Guest.objects.get( pk = pk )
        except Guest.DoesNotExist:
            raise Http404
        
    # GET        
    def get(self , request , pk):
        gest = self.get_object(pk)
        serializer = GuestSerializers(gest)
        return Response(serializer.data , status= status.HTTP_200_OK)
    
    # PUT
    def put(self , request ,pk):
        gest = self.get_object(pk)
        serializer = GuestSerializers(gest , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data , status= status.HTTP_202_ACCEPTED)
        return Response( serializer.errors , status = status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete (self , request , pk):
        gest = self.get_object(pk)
        gest.delete()
        return Response( status= status.HTTP_204_NO_CONTENT)
        