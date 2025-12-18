from library.models import Book
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from library.serializers import BookSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class BookModelTest(TestCase):

    def test_book_creation(self):
        book = Book.objects.create(
            title="Clean Code",
            author="Robert Martin",
            isbn="1234567890",
            available_copies=5,
            page_count=450,
        )
        print("book created")
        self.assertEqual(book.available_copies, 5)

class BookSerializerTest(TestCase):

    def test_valid_serializer(self):
        data = {
            "title": "Atomic Habits",
            "author": "James Clear",
            "isbn": "9876543210",
            "available_copies": 3,
            "page_count": 320,
        }
        print("log the data from test_valid_serializer", data)
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class BookListAPITest(APITestCase):

    def test_get_books(self):
        url = reverse("book-list")
        # print("logged the url", url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# integration tests to verify the main functionalities 
class BookIntegrationTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        # print("pass craet user")
        self.client.force_authenticate(user=self.user)
        
        self.book = Book.objects.create(
            title="Django for APIs",
            author="William Vincent",
            isbn="111222333",
            available_copies=1,
            page_count=300,       
        )
        # print("pass from the book creation")

    def test_borrow_book_flow(self):
        response = self.client.post(
            reverse("borrow-book"),
            {"book_id": self.book.id}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 0)
