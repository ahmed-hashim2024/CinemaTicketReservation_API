"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from tickets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('guests' , views.viewsets_gest)
router.register('movies' , views.viewsets_movie)
router.register('reservations' , views.viewsets_reservation)


urlpatterns = [ 
    path('admin/', admin.site.urls),

    # 1 => # without REST and no model query Function Based View FBV
    path('django/jsonresponcenomodel', views.no_rest_no_model),
    # 2 => # without REST and from model query Function Based View FBV
    path('django/jsonresponcefrommodel', views.no_rest_from_model),
    # 3.1 => GET , POST from rest framework function based view @api_view
    path('rest/fbv', views.FBV_List),
    # 3.1 => GET , PUT , DELETE from rest framework function based view @api_view
    path('rest/fbv/<int:pk>', views.FBV_pk),
    # 4.1 => GET , POST from rest framework class  based view APIView
    path('rest/cbv', views.CBV_list.as_view()),
    # 4.2 => GET , PUT , DELETE from rest framework class  based view APIView
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view()),
    # 5.1 => GET , POST from rest framework mixins based view APIView
    path('rest/mixins', views.mixins_list.as_view()),
    # 5.2 => GET , PUT , DELETE from rest framework mixins  based view APIView
    path('rest/mixins/<int:pk>', views.mixins_pk.as_view()),
    # 6.1 => GET , POST from rest framework generics based view APIView
    path('rest/generics', views.generics_list.as_view()),
    # 6.2 => GET , PUT , DELETE from rest framework generics  based view APIView
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),
    # 7 => GET , post , PUT , DELETE from rest framework viewsets based view APIView
    path('rest/viewsets/', include(router.urls)),
    # 8 => find movie
    path('fbv/findmovie', views.findmovie),
    # 8 => create Reservation
    path('fbv/createreservation' , views.new_reversation), 


]
