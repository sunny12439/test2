from cmath import pi
from collections import UserDict
import email
from multiprocessing import context
from sqlite3 import Date
from tkinter import Entry
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from pyparsing import nestedExpr

from .models import Cluster, Reservation, UserProfile, Users_reservations_dict
from .forms import ClusterForm, RegisterForm, ReservationForm, DateInput
import firstapp

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from firstapp import models
from django.db.models import Q
from django.db import IntegrityError
from django.views.generic.edit import CreateView
#from django.utils import simplejson as json
import json
from django.forms.models import model_to_dict
from .forms import *
from datetime import datetime

def profile(request, user_id):
    
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'firstapp/profile.html', {'user': user})

def profile_update(request, user_id):

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and user_profile_form.is_valid():

            user_form.save()
            user_profile_form.user = user_form
            user_profile_form.save()

            return HttpResponseRedirect(reverse('profile', args=[user_id]))
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'firstapp/profile_update.html', {'user_form': user_form, 'user_profile_form': user_profile_form})

def loggingin(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) 
            if username == 'admin':
                return redirect('Übersicht')
            else:
                return redirect('homestudi')
        else:
            messages.error(request, "Name oder Passwort ist falsch.")
    return render(request, 'firstapp/login.html')


def loggingout(request):
    logout(request)
    return redirect('Login')


"""old register:
def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # create user
            form.save()
            messages.success(request, "Erfolgreich registriert.")
            return redirect('Login')
        else:
            messages.error(
                request, "Registrierung fehlgeschlagen. Bitte erneut versuchen.")
    context = {'form': form}
    return render(request, 'firstapp/register.html', context) """

def register(request):
    form = RegisterForm()
    user_profile_form = UserProfileForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        print(form.is_valid, user_profile_form.is_valid)
        if form.is_valid() and user_profile_form.is_valid():
            # create user
            user = form.save()
            user.save()
            profile = user_profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            messages.success(request, "Registration was successful.")
            return redirect('Login')
        else:
            messages.error(request, "Registration failed. Please try again.")
    context = {'form': form, 'user_profile_form': user_profile_form, }
    return render(request, 'firstapp/register.html', context)



def homepage(request):
    if 'suche' in request.GET:
        suche = request.GET['suche']
        sortieren = Q(Q(tag_system__icontains=suche) | Q( title__icontains=suche) | Q( Beschreibung__icontains=suche))
        cluster = Cluster.objects.filter(sortieren)
    elif 'order_by' in request.GET:
        order_by = request.GET.get('order_by', 'defaultOrderField')
        cluster = Cluster.objects.all().order_by(order_by)
    else:
        cluster = Cluster.objects.all()
    context = {'cluster' : cluster}
    return render(request,'firstapp/homepageAdmin.html', context)

def homepagestudis(request):
    if 'suche' in request.GET:
        suche = request.GET['suche']
        sortieren = Q(Q(tag_system__icontains=suche) | Q( title__icontains=suche) | Q( Beschreibung__icontains=suche))
        cluster= Cluster.objects.filter(sortieren)
    elif 'order_by' in request.GET:
        order_by = request.GET.get('order_by', 'defaultOrderField')
        cluster = Cluster.objects.all().order_by(order_by)
    else:
        cluster = Cluster.objects.all()
    context = {'cluster' : cluster}
    return render(request,'firstapp/homepageStudent.html', context)

def edit(request, cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    form = ClusterForm(request.POST or None, instance=cluster)
    if request.method == "POST":
        if form.is_valid():
            form.save()
        clusterAll = Cluster.objects.all()
        context = {'cluster': clusterAll}
        return render(request, 'firstapp/homepageAdmin.html', context)
    else:
        return render(request, 'firstapp/EditCL.html', {'cluster': cluster, 'form': form})


def new(request):
    form = ClusterForm
    context = {'form': form}
    if request.method == 'POST':
        print(request.POST)
        form = ClusterForm(request.POST)
        if form.is_valid():
            form.save()
        clusterr = Cluster.objects.all()
        contextt = {'cluster': clusterr}
        return render(request, 'firstapp/homepageAdmin.html', contextt)
    else:
        return render(request, 'firstapp/NewCL.html', context)


def deleteCluster(request, cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    cluster.delete()
    return redirect('Übersicht')


def deleteReservation(request, reservation_id):
    res = Users_reservations_dict.objects.get(pk = reservation_id)
    #before deleting set booked slots back to available
    for booked_sl in res.not_av_slots: 
        res.reservation.av_slots.append(booked_sl)
        res.reservation.save()

    res.delete()

    reserved_objs = Users_reservations_dict.objects.filter(user = res.user)
    contextt = {'res_objs': reserved_objs,
                }
    return render(request, 'firstapp/ReservierteTermine.html', contextt)


def deleteSlot(request, reservation_id, slot_value): 
    res = Users_reservations_dict.objects.get(pk = reservation_id)
    for sl in res.not_av_slots: 
        if sl == slot_value:
            res.reservation.av_slots.append(sl)
            res.reservation.save()

            res.not_av_slots.remove(sl)
            res.save()

            reserved_objs = Users_reservations_dict.objects.filter(user = res.user)
            contextt = {'res_objs': reserved_objs,
                        }
            return render(request, 'firstapp/ReservierteTermine.html', contextt)





def impressum(request):
    if request.method == "POST":
        #Daten
        firstname = request.POST['firstname']
        lastsname = request.POST['lastname']
        email = request.POST['email']
        need = request.POST['need']
      # send email 
        send_mail(
           'Contact us from ' + firstname + lastsname,
            need,
            email,
            ['simpleslot30@gmail.com'],

        )
        return render(request, 'firstapp/Impressum.html', {'firstname' : firstname})
    else: 
        return render(request, 'firstapp/Impressum.html')

def remove_dups(list):
    unique_list = []
    for l in list:
        if l not in unique_list:
            unique_list.append(l)
    return unique_list 


def sort_time_lists(listt):     #'08:00 -09:00'
    sort_list = []
    for sl in listt:
        sl_value = datetime.strptime(sl[-5:], '%H:%M').time()
        sort_list.append(sl_value)
    return sorted(sort_list)

def update_reservations(request):
    all_dicts_list = Users_reservations_dict.objects.all()
    current_day = datetime.today().date()
    current_time = datetime.now().time()

    for dict in all_dicts_list:
        if dict.not_av_slots != 0:
            for sl in dict.not_av_slots:
                res_date = datetime.strptime(dict.reservation.date, '%Y-%m-%d').date()
                slot_value = datetime.strptime(sl[-5:], '%H:%M').time()
                if (current_day >= res_date) and  (current_time > slot_value):
                    dict.not_av_slots.remove(sl)
                    dict.save()
                    dict.reservation.av_slots.append(sl)  #if doesn't work properly, try filtering through Reservations.objects() then get concerned reservation and apply changes accordingly
                    dict.reservation.save()
                elif (current_day > res_date):
                    res_id = dict.reservation.id
                    Reservation.objects.get(pk = res_id).delete()


def update_slots(request, slot_value, res_id, user_id):

    current_user = User.objects.get(pk = user_id)

    choosen_Reservation = Reservation.objects.get(pk = res_id)

    users_dict = Users_reservations_dict.objects.filter(reservation = choosen_Reservation, user = current_user)[0]
    users_not_av_list = users_dict.not_av_slots

    choosen_Reservation.av_slots.remove(slot_value)
    choosen_Reservation.save()

    users_not_av_list.append(slot_value)
    users_dict.save()

    reservation_objs = Reservation.objects.all()
    contextt = {'res_objs': reservation_objs,
                'available_slots': sorted(choosen_Reservation.av_slots),
                'res_id': res_id,

                }
    return render(request, 'firstapp/slot_booking.html', contextt)

def whole_day(request, res_id, user_id):
    available_slots = ['08:00 -09:00',
                    '09:30 -10:30',
                    '11:00 -12:00',
                    '12:30 -13:30',
                    '14:00 -15:00',
                    '15:30 -16:30',
                    '17:00 -18:00'
                    ]

    current_user = User.objects.get(pk = user_id)

    choosen_Reservation = Reservation.objects.get(pk = res_id)

    users_dict = Users_reservations_dict.objects.filter(reservation = choosen_Reservation, user = current_user)[0]

    if len(users_dict.reservation.av_slots) == 7:
        choosen_Reservation.av_slots = []
        choosen_Reservation.save()

        users_dict.not_av_slots = available_slots
        users_dict.save()
        
        reservation_objs = Reservation.objects.all()
        contextt = {'res_objs': reservation_objs,
                    'available_slots': sorted(choosen_Reservation.av_slots),
                    'booked_slots': choosen_Reservation.not_av_slots,
                    'res_id': res_id,
                    }
        return render(request, 'firstapp/slot_booking.html', contextt)



def book(request, cluster_id, user_id):
    while True: 
        #update_reservations(request)
        available_slots = ['08:00 -09:00',
                        '09:30 -10:30',
                        '11:00 -12:00',
                        '12:30 -13:30',
                        '14:00 -15:00',
                        '15:30 -16:30',
                        '17:00 -18:00'
                        ]

        cluster = Cluster.objects.get(pk=cluster_id)
        current_user = User.objects.get(pk = user_id)
        res = Reservation()
        res.clusterr = cluster
        res.cluster_title = cluster.title
        res.user = current_user

        form = ReservationForm(request.POST or None, instance=res)
        context = {'form': form,'cluster': cluster,'user': current_user}

        if request.method == 'POST' and form.is_valid:
            # check for Reservation obj with passed cluster
            res_list = Reservation.objects.filter(
                clusterr=cluster, date=request.POST['date'])

            # check if res_list has an obj in it, then create new reservation if necessary or find reservation
            if len(res_list) == 0:
                new_res = Reservation(clusterr=cluster, date=request.POST['date'], not_av_slots=[
                ], av_slots=available_slots, user = current_user)
                new_res.save()

                # create a new object with newly created reservation linked to current_user
                newly_created_res = Reservation.objects.filter(
                    clusterr=cluster, date=request.POST['date'])[0]
                avail_list = newly_created_res.av_slots

                dict = Users_reservations_dict(reservation = newly_created_res, user = current_user, not_av_slots = [])
                dict.save()
                
            else:
                # check if reservation with current user exists
                if len(Users_reservations_dict.objects.filter(reservation = res_list[0], user = current_user)) == 0:
                    dict = Users_reservations_dict(reservation = res_list[0], user = current_user, not_av_slots = [])
                    dict.save()

                avail_list = Users_reservations_dict.objects.filter(reservation = res_list[0], user = current_user)[0].reservation.av_slots
                context = {'available_slots': sorted(avail_list),
                        'picked_date': request.POST['date'],
                        'res_id': res_list[0].id,
                        'reservation': res_list[0],
                        'cluster': cluster,
                        'user': current_user
                        }
                return render(request, 'firstapp/slot_booking.html', context)

        else:
            return render(request, 'firstapp/reservationForm.html', context)

        reservation_objs = Reservation.objects.all()
        contextt = {'res_objs': reservation_objs,
                    'available_slots': sorted(avail_list),
                    'picked_date': request.POST['date'],
                    'res_id': newly_created_res.id,
                    'cluster': cluster,
                    'user': current_user
                    
                    }
        return render(request, 'firstapp/slot_booking.html', contextt)



def ResPage(request, user_id):
    n = User.objects.get(pk=user_id)
    reserved_objs = Users_reservations_dict.objects.filter(user = n)
    contextt = {'res_objs': reserved_objs,
                }
    return render(request, 'firstapp/ReservierteTermine.html', contextt)
    # while True: 
    #     #update_reservations(request)

def ResPageAdmin(request, cluster_id):
    n = Cluster.objects.get(pk=cluster_id)
    reserved_objs = Reservation.objects.filter(clusterr = n)
    contextt = {'reservierte': reserved_objs,
                }
    return render(request, 'firstapp/Reservierungsübersicht.html', contextt)




class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm



# def myreservation(request, user_id):
#     n = User.objects.get(pk=user_id)
#     c = Cluster.objects.all()
#     if 'suche' in request.GET:
#         suche = request.GET['suche']
#         sortieren = Q(Q(cluster__title__icontains=suche) & Q(user=n))
#         reservation = Reservation.objects.filter(sortieren).order_by('cluster', 'date')
#     else:     
#        s = Q(Q(user=n))
#        reservation = Reservation.objects.filter(s).order_by('cluster', 'date')
#     context= {'reservation' : reservation}
#     return render(request,'firstapp/myreservations.html', context)

