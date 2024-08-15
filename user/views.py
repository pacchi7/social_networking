from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .authorization import JWTAuthenticationPermission
from .models import (
    FriendRequest,
    Friendship
)
from .serializers import (
    UserSerializer,
    PendingFriendRequestSerializer,
    UserSignupSerializer,
    UserLoginSerializer
)


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Customize the response here
        response_data = {
            "id": user.id,
            "name": user.first_name,
            "email": user.email,
            "message": "User created successfully!"
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.validated_data
        return Response(response_data, status=status.HTTP_200_OK)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(generics.ListAPIView):
    permission_classes = (JWTAuthenticationPermission,)
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        search_term = self.request.query_params.get('q', '')
        if '@' in search_term:
            queryset = User.objects.filter(email__iexact=search_term)
        else:
            queryset = User.objects.filter(
                Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term)
            )
        return queryset


class SendFriendRequestView(APIView):
    permission_classes = (JWTAuthenticationPermission,)

    def post(self, request, *args, **kwargs):
        import pdb
        pdb.set_trace()
        to_user_id = request.data.get('to_user_id')
        if not to_user_id:
            return Response({"error": "To user ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        from_user = request.user
        check_request_is_existing = FriendRequest.objects.filter(
            Q(from_user=from_user.id)& Q(to_user=to_user_id)
        )
        if check_request_is_existing.exists():
            return Response({"error": "request already exists"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        recent_requests = FriendRequest.objects.filter(
            from_user=from_user,
            created_at__gte=timezone.now() - timezone.timedelta(minutes=1)
        ).count()
        if recent_requests >= 3:
            return Response({"error": "Too many requests"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED)


class AcceptFriendRequestView(APIView):
    permission_classes = (JWTAuthenticationPermission,)

    def post(self, request, *args, **kwargs):
        import pdb
        pdb.set_trace()
        request_id = request.data.get('request_id')
        if not request_id:
            return Response({"error": "Request ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
            
            Friendship.objects.create(user=friend_request.from_user, friend=request.user)
            Friendship.objects.create(user=request.user, friend=friend_request.from_user)
            
            friend_request.delete()
            return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)


class ListPendingRequestsView(APIView):
    permission_classes = (JWTAuthenticationPermission,)

    def get(self, request, *args, **kwargs):
        user = request.user
        pending_requests = FriendRequest.objects.filter(to_user=user)
        serializer = PendingFriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RejectFriendRequestView(APIView):
    permission_classes = (JWTAuthenticationPermission,)

    def post(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        if not request_id:
            return Response({"error": "Request ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
            friend_request.delete()
            return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)


class ListFriendsView(APIView):
    permission_classes = (JWTAuthenticationPermission,)

    def get(self, request, *args, **kwargs):
        user = request.user
        friends = User.objects.filter(
            id__in=User.objects.filter(
                Q(sent_requests__to_user=user) | Q(received_requests__from_user=user)
            ).distinct().values_list('id', flat=True)
        )
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


