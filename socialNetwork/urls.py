from django.urls import path
from .views import UserSearch, FriendRequestView, FriendListView, PendingRequestsView,SignupView, LoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearch.as_view(), name='search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend_request'),
    path('friends/', FriendListView.as_view(), name='friends'),
    path('pending-requests/', PendingRequestsView.as_view(), name='pending_requests'),
]
