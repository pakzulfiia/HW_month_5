from django.urls import path
from . import views

urlpatterns = [
    path('registrate/', views.RegistrationAPIView.as_view()),
    path('authorizate/', views.AuthorizationAPIView.as_view()),
    path('confirm/', views.ConfirmAPIView.as_view())
]