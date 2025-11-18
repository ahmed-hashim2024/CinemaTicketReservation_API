from rest_framework import serializers
from tickets.models import Guest , Movie , Reservation

class MovieSerializers (serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ReservationSerializers (serializers.ModelSerializer):
    class Meta :
        model = Reservation
        fields = '__all__'


class GuestSerializers (serializers.ModelSerializer):
    class Meta :
        model = Guest
        fields = ['pk' , 'Reservation' , 'name' , 'mobile' ]  # عشان يعرض الحجزات بتاعة العميل مع الداتا بتاعة => بجيبها من الكلاس بتاع ال reservation من ال name related 
        