from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    # validates the registration form
    def nameValidator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['lengthFirstName'] = "First name must be at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['first_name']):
            errors['firstNameValid'] = "First name must only contain letters."
        if len(postData['last_name']) < 2:
            errors['lengthLastName'] = "Last name must be at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['last_name']):
            errors['lastNameValid'] = "Last name must only contain letters."
        if len(postData['email']) < 1:
            errors['lengthEmail'] = "Email is required."
        elif not re.match('[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*@[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*(.[A-Za-z]{2,})', postData['email']):
            errors['emailValid'] = "Email not valid."
        elif User.objects.filter(email=postData['email']):
            errors['emailTaken'] = "Email was already registered."
        if len(postData['password']) < 8:
            errors['lengthPassword'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['passConfirmPassword'] = "Passwords do not match."
        return errors

    # validates the login form
    def loginValidator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['noEmail'] = "Please input an email."
        elif not re.match('[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*@[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*(.[A-Za-z]{2,})', postData['email']):
            errors['emaiValid'] = "Email is not valid."
        elif not User.objects.filter(email=postData['email']):
            errors['emailExist'] = "This email is not registered in our database."
        if len(postData['password']) < 1:
            errors['noPass'] = "Please input a password."
        # elif len(postData['password']) < 8:
        #     errors['short_pass'] = "Incorrect password: less than 8 characters."
        elif bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()) == False:
            errors['incorrect_pass'] = "Incorrect password: does not match password stored in database."
        return errors

#User table
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

#book table
class Book(models.Model):
    bookTitle = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#review table linked to the book table and the users table through FK
class Review(models.Model):
    review = models.TextField(max_length=1000)
    rating = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User, related_name="userReviews")
    book= models.ForeignKey(Book, related_name="bookReviews")