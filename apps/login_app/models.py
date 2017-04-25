# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# regex for email validation.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):

    ####################################################################
    # TODO: Change this filter to use '.get' instead and wrap
    # in a try/except block. Check and add code for NO records returned
    # and for TOO MANY records returned.
    ####################################################################
    def find_email(self, data):
        user = User.objects.filter(
            email__exact=data['email']
        )
        return user

    def validate_and_login(self, data):
        print "Inside validate and login"
        # Create a list to hold any errors messages.
        errors = []

        # check the email address with regex.
        if not (EMAIL_REGEX.match(data['email'])) or (len(data['password'])<8):
            errors.append("Login info is invalid")

        # There were errors. Return false and the error dictionary for printing
        # on the html form.
        if errors:
            return (False, errors, data)
        else:

            # If the email that the user is trying to 'register'
            # already exists than we need to 'fail' this registration.
            user = User.objects.find_email(data)
            if user:
                password = data['password'].encode()
                hashed_pw = user[0].password.encode()
            else:
                errors.append("Login info is invalid")
                return (False, errors)

            # Now we can compare the hashed password stored in the
            # database with our 'hashed' copy of the password just entered.
            if not bcrypt.hashpw(password.encode(), hashed_pw) == hashed_pw:
                errors.append("Login info is invalid")
                return (False, errors)

            return (True, user)

    def validate_and_create(self, data):
        print "Inside 'validate_and_create method'"

        # Create a list to hold any errors messages.
        errors = []

        if len(data['first_name'])<2 or len(data['last_name'])<2:
            print "name(s) too short"
            errors.append("First and last names must be at least 2 characters.")

        if len(data['alias'])==0:
            print "Alias is empty. We don't care."

        # check the email address with regex.
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Email must be a valid email address.")

        # Check that password is 8 characters or larger and matches the confirm password field
        if len(data['password'])<8:
            errors.append("Password must be at least 8 characters")

        # Check that the password and confirm password matches
        if not data['password'] == data['confirm_pw']:
            errors.append("Password and confirm password fields must match")

        # Check if this email address is already in the database.
        print "About to print results of find_email"
        print User.objects.find_email(data)
        if User.objects.find_email(data):
            errors.append("A user with that email is already registered.")

        # There were errors. Return false and the error dictionary for printing
        # on the html form.
        if errors:
            return (False, errors, data)

        # Success! Create a new_user object and return True and new_user
        # so the views.py function can add it to the data.
        else:

            # Encrypt the password and store that 'hashed' value into the database.
            password = data['password'].encode()
            pw_hash = bcrypt.hashpw(password, bcrypt.gensalt(14))

            # Add to this info to the database.
            new_user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                alias = data['alias'],
                email = data['email'],
                password = pw_hash  # Store the bcrypt hash into the database.
            )
            print "Added new user to database. About to return"

            return (True, new_user)

# Create your models here.

# TODO: Django has a EmailField type. It should auto check for valid email address. Try it?

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def full_name(self):
        return self.first_name+' '+self.last_name

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
