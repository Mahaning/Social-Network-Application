from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from datetime import timedelta
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = (AllowAny,)  # Allow anyone to access this view

    def post(self, request):
        un = request.data.get('username').lower()  # Convert email to lowercase
        password = request.data.get('password')
        print("Received username:", un)  # Debug print
        print("Received password:", password)  # Debug print
        
        # Authenticate user
        user = authenticate(username=un, password=password)
        print("Authenticated user:", user)  # Debug print
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            print("Generated token:", token.key)  # Debug print
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            print("Invalid credentials")  # Debug print
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserSearch(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('search', '').lower()
        return User.objects.filter(Q(email__iexact=keyword) | Q(username__icontains=keyword) | Q(first_name__icontains=keyword))


class FriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        if not to_user_id:
            return Response({"error": "to_user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        to_user = User.objects.get(id=to_user_id)
        from_user = request.user
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').exists():
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)
        recent_requests = FriendRequest.objects.filter(from_user=from_user, created_at__gte=timezone.now() - timedelta(minutes=1))
        if recent_requests.count() >= 3:
            return Response({"error": "Too many friend requests sent in the last minute"}, status=status.HTTP_400_BAD_REQUEST)
        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user, status='pending')
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        action = request.data.get('action')
        if not request_id or not action:
            return Response({"error": "request_id and action are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request = FriendRequest.objects.filter(id=request_id, to_user=request.user).first()
        if not friend_request:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        if action == 'accept':
            friend_request.status = 'accepted'
        elif action == 'reject':
            friend_request.status = 'rejected'
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_200_OK)

class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = User.objects.filter(Q(sent_requests__to_user=user, sent_requests__status='accepted') |
                                      Q(received_requests__from_user=user, received_requests__status='accepted'))
        return friends

class PendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = FriendRequest.objects.filter(to_user=user, status='pending').select_related('from_user')
        print("Pending requests count:", queryset.count())  # Debug print
        return queryset
