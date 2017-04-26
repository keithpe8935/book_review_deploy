# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse

from models import Book, Review, Author
import datetime

# Create your views here.
def books(request):
    # if user isn't logged in then display the login screen
    if not 'id' in request.session:
        return redirect('login_app:login')

    print "Inside books view"

    context = {
        'books': Book.objects.all().order_by('book_title'),
        'authors': Author.objects.all(),
        'reviews': Review.objects.all(),
        'reviews_short': Review.objects.order_by('-created_at')[:3],
    }

    return render(request,"book_review_app/index.html", context)

def add_book(request):

    # if user isn't logged in then display the login screen
    if not 'id' in request.session:
            return redirect('login_app:login')

    context = {
        'books': Book.objects.all(),
        'authors': Author.objects.all()
    }
    print "Inside add_book view"
    return render(request,"book_review_app/add_book.html",context)

def post_review(request):
    # if user isn't logged in then display the login screen
    if not 'id' in request.session:
        return redirect('login_app:login')

    print "Inside post_review view"
    print "This is a: "+ request.method
    print request.POST

    # We'll need the author to include in the book so we'll create the author (or find an existing author)
    # here, before we need it for book.
    # If the Author First Name and Last name fields are empty we use the one they selected in the pull down
    author = Author.objects.create_author(request.POST)

    # A new book will be created unless the user left the title field in the form empty.
    # Then, we'll use whatever the selected_title field was pointing too.
    book = Book.objects.create_book(request.POST,request.session['id'],author)

    # Add the post with book and author info.
    review = Review.objects.create_review(request.POST, book, author, request.session['id'])

    # Show the book, with author and review
    return redirect('book_review_app:show_book',book.id)

def show_book(request,id):
    # if user isn't logged in then display the login screen
    if not 'id' in request.session:
        return redirect('login_app:login')

    print "Inside show_book view"
    print id
    print request.method
    context = {
         'books': Book.objects.filter(id=id),
         'book': Book.objects.get(id=id),
         'reviews':Review.objects.filter(book_id=id),
         'reviews_by_user':Review.objects.filter(book_id=id).filter(user_id=request.session['id'])
    }
    print context

    return render(request,"book_review_app/show_book.html",context)

def show_user(request,id):
    # if user isn't logged in then display the login screen
    if not 'id' in request.session:
            return redirect('login_app:login')

    print "Inside show_user view"
    print id
    print request.method
    context = {
         'reviews':Review.objects.filter(user_id=id).order_by('book__book_title').distinct(),
         'count': Review.objects.filter(user_id=id).count(),
         'user': Review.objects.filter(user_id=id).first(),
    }
    print context

    return render(request,"book_review_app/show_user.html",context)

# We'll use this when posting against books and authors alreay exist.
#def post_review_only(request,id, book, author_id):
def post_review_only(request,id):
    # if user isn't logged in then display the login screen
    if not 'id' in request.session:
        return redirect('login_app:login')

    print "Inside post_review_for_this_book"
    print id
    print request.method
    print request.POST

    # Grab the book and author
    book = Book.objects.find_book(id);
    author = Author.objects.find_author(book.author_id)

    # Add the post with book and author info.
    review = Review.objects.create_review(request.POST, book, author, request.session['id'])

    context = {
         'books': Book.objects.filter(id=book.id),
         'book': Book.objects.get(id=book.id),
         'reviews':Review.objects.filter(book_id=book.id)
    }
    print context

    return render(request,"book_review_app/show_book.html",context)

#def delete_review(request,id):
def delete_review(request, id):
    # if user isn't logged in then display the login screen
    if not 'id' in request.session:
        return redirect('login_app:login')

    print "Inside the delete_review view"
    print id

    # We want to save the book id for later when we 'return' to show_book
    review = Review.objects.get(id=id);
    b_id = review.book_id;
    print "book ID:"
    print  b_id

    #print request

    # Delete the review with the review id.
    result = Review.objects.delete_review(request.POST, id)

    context = {
         'books': Book.objects.filter(id=b_id),
         'book': Book.objects.get(id=b_id),
         'reviews':Review.objects.filter(book_id=b_id),
         'reviews_by_user':Review.objects.filter(book_id=b_id).filter(user_id=request.session['id'])
    }
    print context

    #return render(request,"book_review_app/show_book.html")
    return render(request,"book_review_app/show_book.html",context)
