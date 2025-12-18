from django.urls import path
from .views import RegisterView, BookListView, BorrowBookView, ReturnBookView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

# here are the routes for auth and borrow/return books 
urlpatterns = [
    #Auth routes
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),

    #Books routes
    path('books/', BookListView.as_view(), name="book-list"),

    path('loans/borrow/', BorrowBookView.as_view(),  name="borrow-book"),
    path('loans/return/', ReturnBookView.as_view(), name="return-book"),
]
