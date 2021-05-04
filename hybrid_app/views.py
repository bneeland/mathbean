from django.http import HttpResponse
from django.views import View

class SessionView(View):
    def get(self, request):
        session = str(self.request.session.session_key)
        cookie = str(request.COOKIES.get('csrftoken'))
        return HttpResponse('<b>Session: </b>' + session + ' <br />' + '<b>Cookie: </b>' + cookie)

from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DocumentSerializer

    def get_queryset(self):
        return self.request.user.documents.all()

    def perform_create(self, serializer):
        kwargs = {
          'user': self.request.user
        }
        
        serializer.save(**kwargs)
