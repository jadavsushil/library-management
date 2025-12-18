from django.contrib import admin
from .models import User, Loan, Book

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Loan)