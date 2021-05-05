from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView

class SessionView(View):
    def get(self, request):
        session = str(self.request.session.session_key)
        cookie = str(request.COOKIES.get('csrftoken'))
        return HttpResponse('<b>Session: </b>' + session + ' <br />' + '<b>Cookie: </b>' + cookie)

class EditorView(TemplateView):
    template_name = "hybrid_app/editor_view.html"

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



from django.views.generic.list import ListView
from django.contrib.auth.models import User
from . import models

class DocumentListView(ListView):
    model = models.Document
    template_name = "hybrid_app/document_list_view.html"
    context_object_name = "documents"

    def get_queryset(self):
        return models.Document.objects.filter(user=self.request.user.id)
