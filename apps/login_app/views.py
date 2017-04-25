# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render,redirect
from models import User

# Create your views here.

# Store all registry entry screen info to session. We can populate the entry
# screen for the user to re-try.
def store_to_session(request):
    request.session['register_first_name']=request.POST['first_name']
    request.session['register_last_name']=request.POST['last_name']
    request.session['register_email']=request.POST['email']
    return

def update_login_session(login,request):
    # Used during login and registration to 'login' the user
    # by storing the 'id','first_name','email' in session
    request.session['id']=login.id
    request.session['first_name']=login.first_name
    request.session['email']=login.email
    return

def index(request):
    print "Inside index def"

    # For displaying all User records (just for testing).
    context = {
        'users': User.objects.all()
    }

    return render(request,"login_app/index.html", context)

def register(request):
    print "Inside register def"
    if request.method=="POST":
        print request.POST

        # validate_and_create returns a tuple: True and the Object,
        # or False and the errors list.
        result = User.objects.validate_and_create(request.POST)
        print result
        if result[0] is True:
            print "Succesful"
            # Clear any session info for this user, including the
            # register_first_name, register_last_name, register_email
            request.session.clear()

            # Now update session with the new registration values.
            update_login_session(result[1],request)
        else:
            print "Unsuccessful."
            # Someone is trying to register, make sure we 'logout' the currently
            # logged in user.
            request.session.clear()

            store_to_session(request);
            for error in result[1]:
                messages.error(request, error)

    return redirect('book_review_app:books')

def login(request):
    print "Inside login def"
    if request.method=="POST":
        print request.POST

        # Someone is trying to login, make sure we 'logout' the currently
        # logged in user.
        request.session.clear()

        result = User.objects.validate_and_login(request.POST)
        if result[0] is True:
            print "Succesful"

            # Store user name, email and id in session,
            # to indicate this user is 'logged' in.
            update_login_session(result[1][0],request)
            return redirect('book_review_app:books')

        else:
            print "Unsuccessful."
            for error in result[1]:
                messages.error(request, error)

    return redirect('login_app:index')

# Clear the session (logout)
def logout(request):
    request.session.clear()
    return redirect('login_app:index')

# For testing: Delete all entries in the login database.
def delete_all(request):
    deleteAll = User.objects.all()
    deleteAll.delete()
    request.session.clear()
    return redirect('login_app:index')

# For testing:  Clear the form
def clear_form(request):
    request.session.clear()
    return redirect('login_app:index')
