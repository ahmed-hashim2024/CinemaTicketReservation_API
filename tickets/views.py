from django.shortcuts import render
from django.http.response import JsonResponse 
from .models import Guest , Reservation , Movie
from rest_framework.decorators import api_view
from .serializers import GuestSerializers ,ReservationSerializers , MovieSerializers
from rest_framework.response import Response
from rest_framework import status , filters 
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics , mixins ,viewsets

# creat auth
from rest_framework.authentication import BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
    
# end auth 


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
        return Response( status = status.HTTP_204_NO_CONTENT)


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
        

# 5 ==> Mixins 
# 5.1 ==> Mixins list 
class mixins_list( mixins.ListModelMixin , mixins.CreateModelMixin , generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

    def get(self, request):
        return self.list(request)
    
    def post(self , request):
        return self.create(request)

# 5.2 ==> Mixins GET , PUT , DELETE 
class mixins_pk(mixins.RetrieveModelMixin , mixins.UpdateModelMixin , mixins.DestroyModelMixin , generics.GenericAPIView) :
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

    def get (self , request , pk):
        return self.retrieve(request)
    
    def put (self , request , pk):
        return self.update(request)
    
    def delete (self , request , pk):
        return self.destroy(request)
    
# 6 ==> Generics
# 6.1 ==> Generics list GET , POST
class generics_list(generics.ListCreateAPIView):
    queryset= Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]     

    # # creat base auth

    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]     
    # # end auth 

# 6.1 ==> Generics list GET , PUT , DELETE 
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset= Guest.objects.all()
    serializer_class = GuestSerializers


# 7 ==> ViewSets

class viewsets_gest (viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

class viewsets_movie (viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets_reservation (viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializers


# 8 ==> find movie
@api_view(['GEt'])
def findmovie(request):
    movies = Movie.objects.filter(
        hall = request.data ['hall'],
        movie = request.data ['movie'],
    )
    serializer = MovieSerializers(movies , many = True)
    return Response(serializer.data)


# 9 ==>  create new reversation 

@api_view(['post'])
def new_reversation(request):

    movie = Movie.objects.get(
        movie = request.data['movie'],
        hall = request.data['hall']
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response( status= status.HTTP_201_CREATED)

















