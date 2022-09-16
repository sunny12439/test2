from django.urls import path, reverse_lazy
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from . import views
urlpatterns = [
    path('homepage/', views.homepage, name='Übersicht'),
    path('impressum/', views.impressum, name='Impressum'),
    path('new/', views.new, name='New'),
    path('edit/<cluster_id>', views.edit, name='edit'),
    path('deleteCluster/<cluster_id>', views.deleteCluster, name='deleteCluster'),
    path('deleteReservation/<reservation_id>', views.deleteReservation, name='deleteReservation'),
    path('cls/', views.homepagestudis, name='homestudi'),
    path('', views.loggingin, name='Login'),
    path('logout/', views.loggingout, name='Logout'),
    path('register/', views.register, name='Register'),
    # path('reservation/<cluster_id>/<user_id>', views.reservation, name='bookSlot'),
    # path('myreservations/<user_id>', views.myreservation, name='MyReservations'),

    path('change_password/', PasswordChangeView.as_view(
        template_name='firstapp/change_password.html',
        success_url= reverse_lazy('password_change_done')), name = "password_change"),
    path('change_password/done/', PasswordChangeDoneView.as_view(
        template_name='firstapp/password_change_done.html'
    ), name="password_change_done"),
    path('profile/<user_id>', views.profile, name='profile'),
    path('profile/update/<user_id>', views.profile_update, name='profile_update'),
    path('book/<cluster_id>/<int:user_id>', views.book, name='book'),
    path('respage/<int:user_id>', views.ResPage, name='ResPage'),
    path('update_slots/<str:slot_value>/<int:res_id>/<int:user_id>', views.update_slots, name='update_slots'),
    path('whole_day/<int:res_id>/<int:user_id>', views.whole_day, name='whole_day'),
    path('deleteSlot/<int:reservation_id>/<str:slot_value>', views.deleteSlot, name='deleteSlot'),
    path('AdminResControl', views.AdminResControl, name='AdminResControl'),
    path('deleteResAdmin/<reservation_id>', views.deleteResAdmin, name='deleteResAdmin'),


]
