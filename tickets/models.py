from django.db import models

# Guest -- Movie -- Reservation

class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=10 )
    date = models.DateField()
     

class Guest(models.Model):
     name = models.CharField(max_length=20)
     mobile = models.IntegerField(max_length=12)

class Reservation(models.Model):
      guest = models.ForeignKey(Guest , related_name='Reservation', on_delete = models.CASCADE) 
      movie = models.ForeignKey(Movie , related_name='Movie', on_delete = models.CASCADE)