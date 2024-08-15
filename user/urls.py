from django.urls import path
from .views import (
    UserSignupView,
    UserLoginView,
    UserSearchView,
    SendFriendRequestView,
    AcceptFriendRequestView,
    ListPendingRequestsView,
    RejectFriendRequestView,
    ListFriendsView
)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user_search'),
    path('send_friend_request/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept_friend_request/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('list_pending_requests/', ListPendingRequestsView.as_view(), name='list_pending_requests'),
    path('reject_friend_request/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('list_friends/', ListFriendsView.as_view(), name='list_friends'),
]
