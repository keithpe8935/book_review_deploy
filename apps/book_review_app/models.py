# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_app.models import User
# Create your models here.

class BookManager(models.Manager):

    # Find Book by it's ID
    def find_book(self, id):
        print "We are searching for this already existing author"
        print id

        try:
            book = Book.objects.get(id=id)
            print "we found the Book!"

        except Exception as e:
            print 'There were problems'
            print '%s (%s)' % (e.message,type(e))
            return false;

        return book

    def create_book(self, data, userid, author):

        # If the 'new' title field is empty it means the user selectd an existing book
        # to write a review for

        if data['title']=='':
            title = data['selected_title']
            print "We're searching for this title:"+title

            # If the book_title field is empty use the 'selected_title field'
            try:
                #book = Book.objects.filter(book_title=title)
                book = Book.objects.get(book_title=title)
                print "******The title found is: "
                print book.book_title
                print "******"
                print "all is well"

            except Exception as e:
                print "there were problems."
                print '%s (%s)' % (e.message, type(e))

        else:
            # We'll create a new book with what's in the title field of the form
            try:
                book = Book(book_title = data['title'], author_id=author.id)
                book.save()
                print 'all is well'

            except Exception as e:
                print '%s (%s)' % (e.message, type(e))
                return false

        return book


class AuthorManager(models.Manager):

    # Find an author by his id
    def find_author(self, id):
        print "We are searching for this already existing author"
        print id

        try:
            author = Author.objects.get(id=id)
            print "we found the author!"

        except Exception as e:
            print 'There were problems'
            print '%s (%s)' % (e.message,type(e))
            return false;

        return author

    def create_author(self, data):

        print "Inside create_author (in models)"
        print data

        if data['first_name']=='':
            print "We are searching for this already existing author"
            print data['first_name']
            print data['last_name']
            try:
                author = Author.objects.get(id=data['selected_author_id'])
                print "we found the author!"

            except Exception as e:
                print 'There were problems'
                print '%s (%s)' % (e.message,type(e))

        else:

            # Create the author and attach it to the book
            # Check if the user selected an existing author (first_name last name field blank)
            # Look up author from select list, find it in table and add book to it.
            try:
                print "The next line should print the author name"
                print data['first_name']
                print data['last_name']

                # See if the author is already in the Author table
                # return the first one we find.
                author = Author.objects.filter(first_name__iexact=data['first_name'].strip()).filter(last_name__iexact=data['last_name'].strip())
                if author:
                    return author[0]

                if not author:
                    author = Author(first_name=data['first_name'],last_name=data['last_name'])
                    author.save()

            except Exception as e:
                print 'There were problems'
                print '%s (%s)' % (e.message, type(e))

        return author

class ReviewManager(models.Manager):

    def delete_review(self, data, id):
        print "Inside the delete_review method of ReviewManager"
        #print data
        print id

        try:
            result = Review.objects.get(id=id)
            result.delete()
            print "Review "+id+" deleted successfully"

        except Exception as e:
            print 'There were problems'
            print '% (%)' % (e.message, type(e))
            return False;

        return True

    def create_review(self, data, book, author, userid):
        print "Inside create_review (in models)"
        print data

        # Get the current user id. We want to add that to the review
        print "Is the next line the user id"
        print userid
        # Create and attach review
        try:
            print "The next line should print the textof the review"
            print data['review']
            print data['rating']
            review = Review(review=data['review'],rating=data['rating'],book_id=book.id, user_id=userid)
            review.save()
            print 'Review Created successfully'

        except Exception as e:
            print 'There were problems'
            print '%s (%s)' % (e.message, type(e))

        return review

        # Now return the book with the author and review attached (well, linked anyway).
        # TODO: Do I want this next line (review.book = book)?
        #review.book = book
        #return book
        #return book[0]
        #return

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()

    def full_name(self):
        return self.first_name+' '+self.last_name
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Book(models.Model):
    book_title = models.CharField(max_length=50)
    isbn = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books',related_query_name='book')
    objects = BookManager()

class Review(models.Model):
    review = models.CharField(max_length=255)
    rating = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', related_query_name='review')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', related_query_name='review')
    objects = ReviewManager()
