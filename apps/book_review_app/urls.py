from django.conf.urls import url, include
from django.contrib import admin
import views

app_name = 'book_review_app'
urlpatterns = [
    url(r'^$', views.books, name='books' ),
    url(r'^add$', views.add_book, name='add_book' ),
    url(r'^post$', views.post_review, name='post_review' ),
    url(r'^user/(?P<id>\d+)$', views.show_user, name='show_user' ),
    url(r'^review/(?P<id>\d+)/delete$', views.delete_review, name='delete_review' ),
    url(r'^(?P<id>\d+)/post$', views.post_review_only, name='post_review_only' ),
    url(r'^(?P<id>\d+)/show$', views.show_book, name='show_book' ),
]
