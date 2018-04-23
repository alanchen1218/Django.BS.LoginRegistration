from django.shortcuts import render, redirect
from .models import *
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.contrib import messages
  # the index function is called when root is visited
def index(request):
  return render(request, 'first_app/index.html')

def register(request):
  errors = User.objects.nameValidator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
      request.session['first_name'] = request.POST['first_name']
      request.session['last_name'] = request.POST['last_name']
      request.session['email'] = request.POST['email']
      return redirect('/')
  else:
    pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pwhash)
    request.session['first_name'] = request.POST['first_name']
    request.session['last_name'] = request.POST['last_name']
    return redirect('/home')

def login(request):
  errors = User.objects.loginValidator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/')
  else:
    request.session['id'] = User.objects.get(email=request.POST['email']).id
    request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
    request.session['last_name'] = User.objects.get(email=request.POST['email']).last_name
    return redirect('/home')
  
def success(request):
  return render(request, 'first_app/success.html')

def home(request):
  if not 'first_name' in request.session:
    return redirect('/')
  # print(request.session['id'])
  else:
    reviews = Review.objects.all()
    books = Book.objects.all()
    context = {
      'reviews' : reviews,
      'books' : books
    }
    return render(request, 'first_app/home.html',context)

def logout(request):
    request.session.clear()
    return redirect('/')

def addBook(request):
  print(Review.user_id)
  if not 'first_name' in request.session:
    return redirect('/')
  else:
    if request.method == 'POST':
      if not Book.objects.filter(bookTitle = request.POST['bookTitle'], author = request.POST['author']):
        Book.objects.create(bookTitle = request.POST['bookTitle'], author = request.POST['author'])
        book = Book.objects.get(bookTitle = request.POST['bookTitle'], author = request.POST['author'])
        book.bookReviews.create(review = request.POST['review'], rating = request.POST['rating'], user_id = request.session['id'])
        return redirect('/home', kwargs={'id' : book.id})
  books = Book.objects.all()
  context = {
    'books': books
  }
  return render(request, 'first_app/addBook.html', context)

def show(request, number):
  if not 'first_name' in request.session:
    return redirect('/')
  else:
    book = Book.objects.get(id=number)
    reviews = book.bookReviews.all()
    context = {
      'book' : book,
      'reviews' : reviews
    }  
    return render(request, 'first_app/bookReviews.html', context)

def createReview(request, number):
  if not 'first_name' in request.session:
    return redirect('/')
  else:
    Review.objects.create(review=request.POST['newReview'], rating=request.POST['rating'],book_id=number,user_id=request.session['id'])
    return redirect('/home', kwargs={'id':id})

def user(request, number):
  if not 'first_name' in request.session:
    return redirect('/')
  else:
    user = User.objects.get(id=number)
    reviews = user.userReviews.all()
    total = len(reviews)
    context = {
      'user' : user,
      'reviews' : reviews,
      'total' : total 
    }
    return render(request, 'first_app/userReview.html', context)

def destroy(request, number):
  if not 'first_name' in request.session:
    return redirect('/')
  else:
    Review.objects.get(id=number).delete()
    return redirect('/home')