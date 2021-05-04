from django.urls import path
from . import views

urlpatterns = [
    path('', views.SessionView.as_view(), name="SessionView"),
]
