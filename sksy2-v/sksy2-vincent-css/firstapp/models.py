from unicodedata import name
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Cluster(models.Model):
    tag_choice = (
        ('Art' , 'Art'),
        ('Chemistry' , 'Chemistry'),
        ('Technical Devices' , 'Technical Devices'),
        ('Cooking' , 'Cooking'),
        ('Music' , 'Music'),
    )
    
    tag_system = models.CharField(max_length=30, blank=True, choices=tag_choice)
    title = models.CharField(max_length=250)
    Beschreibung = models.CharField(max_length=250)
    availability = models.BooleanField()  

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    matrikelnummer = models.IntegerField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=128, blank=True, null=True)
    mod_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return "{}".format(self.user.__str__())


class Reservation(models.Model):
    clusterr = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    cluster_title = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    not_av_slots = models.JSONField(null=True)
    av_slots = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['clusterr', 'date'], name='unique_reservation')
        ]

    def __str__(self):
        return self.user.username


class Users_reservations_dict(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    not_av_slots = models.JSONField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['reservation', 'user'], name='unique_user_reservation')
        ]

# (changes in database:)
#python manage.py makemigrations --> python manage.py migrate

# ('no such tables' error:)
#python manage.py makemigrations --> python manage.py migrate --run-syncdb