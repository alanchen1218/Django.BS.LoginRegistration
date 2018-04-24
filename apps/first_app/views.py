from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Q
import bcrypt
from .models import *

# the index function is called when root is visited
def index(request):
  return render(request, 'first_app/index.html')

def register(request):
  errors = User.objects.nameValidator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
      request.session['fullname'] = request.POST['fullname']
      request.session['username'] = request.POST['username']
      return redirect('/')
  else:
    pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(fullname = request.POST['fullname'], username = request.POST['username'], password = pwhash)
    request.session['fullname'] = request.POST['fullname']
    return redirect('/dashboard')

def login(request):
  errors = User.objects.loginValidator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/')
  else:
    request.session['fullname'] = User.objects.get(username=request.POST['username']).fullname
    request.session['id'] = User.objects.get(username=request.POST['username']).id
    print (request.session['id'])
    return redirect('/dashboard')
  

# def dashboard(request):
#   currentUser = User.objects.get(id = request.session['id'])
#   context = {
#     'wishlist' : Wishlist.objects.all(),
#     'otherliked' : Wishlist.objects.filter(~Q(liked_users=currentUser)),
#     'liked' : Wishlist.objects.filter(liked_users = currentUser)
#   }
#   liked = {}
#   return render(request, 'first_app/dashboard.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

# def create(request):
#   return render(request, 'first_app/create.html')

# def createrender(request):
#   errors = Wishlist.objects.WishManager(request.POST)
#   if (errors):
#     for key, value in errors.items():
#       messages.error(request, value)
#     return redirect('/wish_items/create')
#   else:
#     Wishlist.objects.create(name = request.POST['name'],added_by = User.objects.get(id=request.session['id']))
#     return redirect('/dashboard')

# def destroy(request, number):
#   Wishlist.objects.get(id=number).delete()
#   return redirect('/dashboard')

# def wishItem(request, number):
#   user = User.objects.get(id=number)
#   item = Wishlist.objects.get(id=number)
#   context = {
#     'user' : user,
#     'item' : item
#   }
#   return render(request, 'first_app/info.html', context)

# def add(request, number):
#    User.objects.get(id=request.session['id']).liked_items.add(Wishlist.objects.get(id=number))
#    return redirect('/dashboard')

# def show(request, number):
#   context = {
#     'item' : Wishlist.objects.get(id=itemid),
#     'likedusers' : Wishlist.objects.get(id=number).liked_users.all().values('first_name')
#   }
#   return render(request, 'first_app/info.html', context)
