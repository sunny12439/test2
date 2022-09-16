from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Cluster(models.Model):
    title = models.CharField(max_length=250)
    quantity = models.PositiveIntegerField(default=0,
                validators=[MaxValueValidator(1),MinValueValidator(0)])
    duration= models.PositiveIntegerField()
    availability = models.DateField()

class freeDates(models.Model):
    date = models.DateField()   

# not used yet, using the defaul "User" model from django
class Nutzer(models.Model):
    matrikelnummer = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=64)
    def str(self):
        return '%s'%self.username


class Todo(models.Model):
    title = models.CharField(max_length=250)
    deadline = models.DateField()
    percent = models.PositiveIntegerField(default=0,
                validators=[MaxValueValidator(100),MinValueValidator(0)])


#python manage.py makemigrations --> python manage.py migrate
