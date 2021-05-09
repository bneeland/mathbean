from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import models
from . import serializers

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

class BlockEditAPI(APIView):
    def get(self, request, pk, format=None):
        blocks = models.Block.objects.filter(document__id=self.kwargs['pk'])
        serializer = serializers.BlockSerializer(blocks, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = serializers.BlockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(document=models.Document.objects.get(pk=self.kwargs['pk']))
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # if serializer.is_valid():
        #     instance = serializer.save(commit=False)
        #     instance.document = self.kwargs['pk']
        #     instance.save()

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
