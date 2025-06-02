from django.urls import path
from userprofile.views import ProfileView, ProfileDetailView


urlpatterns = [
    path('profiles/', ProfileView, name='profiles'),
    path('profiles/<int:pk>/', ProfileDetailView, name='profile_detail'),
]