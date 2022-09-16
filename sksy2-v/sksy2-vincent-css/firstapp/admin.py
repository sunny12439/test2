from django.contrib import admin
from .models import Cluster, Reservation, UserProfile, Users_reservations_dict

# Register your models here.
admin.site.register(Cluster)
admin.site.register(Reservation)
admin.site.register(UserProfile)
admin.site.register(Users_reservations_dict)