from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import api
urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('editprofile/', api.editprofile, name='editprofile'),
    path('changepassword/', api.changepassword, name='changepassword'),
    path('friends/suggestions/', api.my_friend_suggestions, name='my_friend_suggestions'),
    path('friends/<uuid:pk>/', api.friends, name="friends"), #this is how you see friends
    path('friends/<uuid:pk>/request/', api.send_friend_request, name='send_friend_request'),  # this is how you send friend request
    path('friends/<uuid:pk>/<str:status>/', api.handle_request, name='handle_request'),
]
