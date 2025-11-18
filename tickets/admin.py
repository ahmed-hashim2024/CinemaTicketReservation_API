from django.contrib import admin
from .models import Guest , Reservation , Movie


admin.site.register(Guest)
admin.site.register(Reservation)
admin.site.register(Movie)