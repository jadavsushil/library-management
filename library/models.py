from django.db import models
from django.contrib.auth.models import AbstractUser

# ADDed below extended Django User model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')

    def is_admin(self):
        return self.role == 'ADMIN'

# here is  the books model 
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    page_count = models.PositiveIntegerField()
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# here is the Loan model for the book 
class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'book', 'is_active')
