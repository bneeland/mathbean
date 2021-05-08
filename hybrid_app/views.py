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
from rest_framework import generics
from . import serializers
from . import models

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DocumentSerializer

    def get_queryset(self):
        return self.request.user.documents.all()

    def perform_create(self, serializer):
        kwargs = {'user': self.request.user}
        serializer.save(**kwargs)

class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BlockSerializer

    def get_queryset(self):
        return self.request.user.blocks.all()

    def perform_create(self, serializer):
        kwargs = {'user': self.request.user}
        serializer.save(**kwargs)

# class BlockAPIView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.BlockSerializer
#
#     def get_queryset(self):
#         return models.Block.objects.filter(document_pk=self.kwargs['pk'])

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BlockViewSet2(APIView):
    def get(self, request, pk, format=None):
        blocks = models.Block.objects.filter(document__id=self.kwargs['pk'])
        serializer = serializers.BlockSerializer(blocks, many=True)
        return Response(serializer.data)


from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import models

class DocumentListView(LoginRequiredMixin, ListView):
    login_url = 'account_login'

    model = models.Document
    template_name = "hybrid_app/document_list_view.html"
    context_object_name = "documents"

    def get_queryset(self):
        return models.Document.objects.filter(user=self.request.user.id)

class DocumentEditView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = 'account_login'

    template_name = "hybrid_app/document_edit_view.html"

    def test_func(self):
        return models.Document.objects.filter(pk=self.kwargs['pk'])[0].user == self.request.user
