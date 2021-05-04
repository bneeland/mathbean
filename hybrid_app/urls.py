from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter()
router.register('documents', views.DocumentViewSet, 'documents')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.SessionView.as_view(), name="SessionView"),
]
