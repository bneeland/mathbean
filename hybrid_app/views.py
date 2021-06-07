from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

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
        serializer.save(user=self.request.user)

    # def update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return super().update(request, *args, **kwargs)

class BlockEditAPI(APIView):
    def get(self, request, pk, format=None):
        blocks = models.Block.objects.filter(document__id=self.kwargs['pk']).order_by('order', 'id')
        serializer = serializers.BlockSerializer(blocks, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = serializers.BlockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                document=models.Document.objects.get(pk=self.kwargs['pk']),
                user=self.request.user,
                order=99,
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoveBlockAPI(UpdateAPIView):
    def get_object(self, pk):
        return models.Block.objects.get(pk=pk)

    def patch(self, request, direction, pk, format=None):
        print("direction: ", self.kwargs['direction'])
        print("pk: ", self.kwargs['pk'])

        block_a = self.get_object(pk)
        order_a_old = block_a.order

        if direction == "up":
            order_b_old = order_a_old - 1
        elif direction == "down":
            order_b_old = order_a_old + 1
        block_b = models.Block.objects.get(order=order_b_old)
        order_a_new = order_b_old
        order_b_new = order_a_old
        # block_a.order = order_a_new
        # block_b.order = order_b_new

        serializer_a = serializers.BlockSerializer(block_a, data={}, partial=True)
        serializer_b = serializers.BlockSerializer(block_b, data={}, partial=True)

        if serializer_a.is_valid() and serializer_b.is_valid():
            serializer_a.save(
                order=order_a_new,
                next_block_pk=block_b.pk,
            )
            serializer_b.save(
                order=order_b_new,
            )
            print("serializer_a:", serializer_a.data)
            return Response(serializer_a.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentListView(LoginRequiredMixin, ListView):
    login_url = 'account_login'

    model = models.Document
    template_name = "hybrid_app/document_list_view.html"
    context_object_name = "documents"

    def get_queryset(self):
        return models.Document.objects.filter(user=self.request.user.id)

class CreateDocumentView(LoginRequiredMixin, RedirectView):
    login_url = 'account_login'

    def get_redirect_url(self, *args, **kwargs):
        document = models.Document.objects.create(name="Untitled document", user=self.request.user)
        return reverse_lazy("hybrid_app:document_edit_view", args=[document.pk])

class DocumentEditView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = 'account_login'

    template_name = "hybrid_app/document_edit_view.html"

    def test_func(self):
        return models.Document.objects.get(pk=self.kwargs['pk']).user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document'] = models.Document.objects.get(pk=self.kwargs['pk'])
        return context

from django.views.generic.edit import CreateView

class BlockCreateView(CreateView):
    model = models.Block
    fields = "__all__"
    template_name = "hybrid_app/block_create_view.html"
    success_url = reverse_lazy("hybrid_app:block_create_view")





class TestView(TemplateView):
    template_name = "hybrid_app/test_view.html"
