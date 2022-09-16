from django.contrib import admin
from .models import Cluster,Todo

# Register your models here.
admin.site.register(Todo)
admin.site.register(Cluster)
