from ast import Pass
from sre_constants import SUCCESS
from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordChangeView


from . import views
urlpatterns = [
    path('homepage/', views.homepage, name='Übersicht'),
    path('impressum/', views.impressum, name='Impressum'),
    path('new/', views.new, name='New'),
    path('edit/<cluster_id>', views.edit, name='edit'),
    path('delete/<cluster_id>', views.delete, name='delete'),
    path('cls/', views.homepagestudis, name='homestudi'),
    path('', views.loggingin, name='Login'),
    path('logout/', views.loggingout, name='Logout'),
    path('register/', views.register, name='Register'),
    path('editProfil/<user_id>', views.editProfil, name='EditProfil'),
    path('change_password/', PasswordChangeView.as_view(), name= 'password_change'),

]

