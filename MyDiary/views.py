# Imports
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Tag, DiaryEntry
from .serializers import TagSerializer, DiaryEntrySerializer
from datetime import datetime


# Register User View
@api_view(['POST'])
def register_user(request):
    try:
        data = request.data
        username = data.get("username")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # Password validation
        if password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password)  # Hashing the password
        )

        return Response({"message": "User registered successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Login User View
@api_view(['POST'])
def login_user(request):
    try:
        data = request.data
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful.",
                "token": token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# List all Tags or Create a new Tag
class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, Update, or Delete a specific Tag
class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Tag deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# List all DiaryEntries or Create a new DiaryEntry
class DiaryEntryListCreateView(generics.ListCreateAPIView):
    queryset = DiaryEntry.objects.all()
    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Retrieve, Update, or Delete a specific DiaryEntry
class DiaryEntryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiaryEntry.objects.all()
    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

@api_view(['GET'])
def search_diaries(request):
    try:
        query = request.GET.get("query", "").strip()  # Search by title or content
        start_date = request.GET.get("startDate", "").strip()  # Start date (DD/MM/YYYY)

        # If both query and start_date are empty, return an error
        if not query and not start_date:
            return Response({"error": "Please provide either a query or a start date."}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize queryset
        diaries = DiaryEntry.objects.all()

        # Filter by query (title or content) if provided
        if query:
            diaries = diaries.filter(title__icontains=query)  # Search by title (case-insensitive)
            diaries |= diaries.filter(content__icontains=query)  # Also search by content (case-insensitive)
        
        # Filter by start date if provided
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
                diaries = diaries.filter(entry_date=start_date_obj)  # Filter by exact date
            except ValueError:
                return Response({"error": "Invalid start date format. Please use DD/MM/YYYY."}, status=status.HTTP_400_BAD_REQUEST)

        # If no diary entries are found, return a not found message
        if not diaries.exists():
            return Response({"message": "No diary entries found for the given query or date."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the filtered diary entries
        serializer = DiaryEntrySerializer(diaries, many=True)

        return Response({"results": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)