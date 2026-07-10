from django.urls import path
from . import views

urlpatterns = [
    path('registrate/', views.registration_api_view),
    path('authorizate/', views.authorization_api_view),
    path('confirm/', views.confirm_api_view)
]