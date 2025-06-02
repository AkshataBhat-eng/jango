from django.urls import path
from .views import get_profile, update_email, hello_world, ProfileView

urlpatterns = [
    path('hello/', hello_world, name='hello-world'),
    path('name/', ProfileView, name='profile'),
    path('profile/<str:name>/', get_profile, name='get_profile'),
    path('profile/<str:name>/email', update_email, name='update_email')
]