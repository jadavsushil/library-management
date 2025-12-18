from .models import Book, Loan
from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response  import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer, BookSerializer, BorrowBookSerializer, ReturnBookSerializer

class HomeView(APIView):
    def get(self, request):
        print("Starting Backend ")
        return Response({"message": "Library API running"})

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'isbn']

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer
    )

    def post(self, request):
        # print("logging the data" , request.data)
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )

class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BorrowBookSerializer
    )

    def post(self, request):
        print("data", request.data)
        serializer = BorrowBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data['book_id']
        # print("bookId", book_id)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if book.available_copies <= 0:
            return Response(
                {"error": "Book is not available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Loan.objects.filter(
            user=request.user,
            book=book,
            is_active=True
        ).exists():
            return Response(
                {"error": "You have already borrowed this book"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Loan.objects.create(
            user=request.user,
            book=book
        )

# Updating the availability of book after the borrowing the book
        book.available_copies -= 1
        book.save()

        return Response(
            {"message": "Book borrowed successfully"},
            status=status.HTTP_201_CREATED
        )

class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ReturnBookSerializer
    )

    def post(self, request):
        serializer = ReturnBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data['book_id']
        # print("return book id " , book_id)
        try:
            loan = Loan.objects.get(
                user=request.user,
                book_id=book_id,
                is_active=True
            )
        except Loan.DoesNotExist:
            return Response(
                {"error": "No active loan found for this book"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # make loan activness is false after returning the book
        loan.is_active = False
        loan.returned_at = timezone.now()
        loan.save()

        # increasing the book copies 
        book = loan.book
        book.available_copies += 1
        book.save()

        return Response(
            {"message": "Book returned successfully"},
            status=status.HTTP_200_OK
        )
