from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework import status
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Min, Max

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from . import models
from . import serializers

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DocumentSerializer

    def get_queryset(self):
        return self.request.user.documents.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BlockSerializer

    def get_queryset(self):
        return self.request.user.blocks.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BlockEditAPI(APIView):
    def get(self, request, pk, format=None):
        blocks = models.Block.objects.filter(document__id=self.kwargs['pk']).order_by('order', 'id')
        serializer = serializers.BlockSerializer(blocks, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = serializers.BlockSerializer(data=request.data)
        if serializer.is_valid():
            try:
                max_block_order = models.Block.objects.filter(document__id=self.kwargs['pk']).aggregate(Max('order'))['order__max']
                order = max_block_order + 1
            except:
                order = 0
            serializer.save(
                document=models.Document.objects.get(pk=self.kwargs['pk']),
                user=self.request.user,
                order=order,
                max_block_order=max_block_order,
            )

            document=models.Document.objects.get(pk=self.kwargs['pk'])
            document.max_block_order = max_block_order
            document.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoveBlockAPI(UpdateAPIView):
    def get_object(self, pk):
        return models.Block.objects.get(pk=pk)

    def patch(self, request, direction, document_pk, pk, format=None):
        block_a = self.get_object(pk)
        order_a_old = block_a.order

        min_block_order = models.Block.objects.filter(document__id=self.kwargs['document_pk']).aggregate(Min('order'))['order__min']
        max_block_order = models.Block.objects.filter(document__id=self.kwargs['document_pk']).aggregate(Max('order'))['order__max']

        # if (direction == "up" and order_a_old != min_block_order) or (direction == "down" and order_a_old != max_block_order):
        if direction == "up":
            order_b_old = models.Block.objects.filter(
                document__id=self.kwargs['document_pk']
            ).filter(
                order__lt=order_a_old
            ).order_by('order').last().order
        elif direction == "down":
            order_b_old = models.Block.objects.filter(
                document__id=self.kwargs['document_pk']
            ).filter(
                order__gt=order_a_old
            ).order_by('order').first().order

        block_b = models.Block.objects.get(order=order_b_old)
        order_a_new = order_b_old
        order_b_new = order_a_old

        serializer_a = serializers.BlockSerializer(block_a, data={}, partial=True)
        serializer_b = serializers.BlockSerializer(block_b, data={}, partial=True)

        if serializer_a.is_valid() and serializer_b.is_valid():
            serializer_a.save(
                order=order_a_new,
                # Add pk of block_b, which has changed order too, for frontend to manage
                next_block_pk=block_b.pk,
            )
            serializer_b.save(
                order=order_b_new,
            )
            return Response(serializer_a.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(None)

class DeleteBlockAPI(DestroyAPIView):
    def get_object(self):
        return models.Block.objects.get(pk=self.kwargs['pk'])

    def destroy(self, request, document_pk, pk, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        min_block_order = models.Block.objects.filter(document__id=self.kwargs['document_pk']).aggregate(Min('order'))['order__min']
        max_block_order = models.Block.objects.filter(document__id=self.kwargs['document_pk']).aggregate(Max('order'))['order__max']
        document=models.Document.objects.get(pk=document_pk)
        document.min_block_order = min_block_order
        document.max_block_order = max_block_order
        document.save()

        data = {
            min_block_order: min_block_order,
            max_block_order: max_block_order
        }

        return Response(data, status=status.HTTP_204_NO_CONTENT)

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
        document = models.Document.objects.create(name="Untitled document", user=self.request.user, min_block_order=0, max_block_order=0)
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

class StudentListListView(LoginRequiredMixin, ListView):
    login_url = 'account_login'

    model = models.StudentList
    template_name = "hybrid_app/student_list_list_view.html"
    context_object_name = "student_lists"

    def get_queryset(self):
        return models.StudentList.objects.filter(user=self.request.user.id)

class CreateStudentListView(LoginRequiredMixin, CreateView):
    login_url = 'account_login'

    model = models.StudentList
    fields = ['name', 'students', ]
    template_name = "hybrid_app/create_student_list_view.html"
    success_url = reverse_lazy("hybrid_app:student_list_list_view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateStudentListView(LoginRequiredMixin, UpdateView):
    login_url = 'account_login'

    model = models.StudentList
    fields = ['name', 'students', ]
    template_name = "hybrid_app/update_student_list_view.html"
    success_url = reverse_lazy("hybrid_app:student_list_list_view")

class StudentListView(LoginRequiredMixin, ListView):
    login_url = 'account_login'

    model = models.Student
    template_name = "hybrid_app/student_list_view.html"
    context_object_name = "students"

    def get_queryset(self):
        return models.Student.objects.filter(user=self.request.user.id)

class CreateStudentView(LoginRequiredMixin, CreateView):
    login_url = 'account_login'

    model = models.Student
    fields = ['email', ]
    template_name = "hybrid_app/create_student_view.html"
    success_url = reverse_lazy("hybrid_app:student_list_view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateStudentView(LoginRequiredMixin, UpdateView):
    login_url = 'account_login'

    model = models.Student
    fields = ['email', ]
    template_name = "hybrid_app/update_student_view.html"
    success_url = reverse_lazy("hybrid_app:student_list_view")

class TeacherListView(LoginRequiredMixin, ListView):
    login_url = 'account_login'

    model = models.Teacher
    template_name = "hybrid_app/teacher_list_view.html"
    context_object_name = "teachers"

    def get_queryset(self):
        return models.Teacher.objects.filter(user=self.request.user.id)

class CreateTeacherView(LoginRequiredMixin, CreateView):
    login_url = 'account_login'

    model = models.Teacher
    fields = ['email', ]
    template_name = "hybrid_app/create_teacher_view.html"
    success_url = reverse_lazy("hybrid_app:teacher_list_view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateTeacherView(LoginRequiredMixin, UpdateView):
    login_url = 'account_login'

    model = models.Teacher
    fields = ['email', ]
    template_name = "hybrid_app/update_teacher_view.html"
    success_url = reverse_lazy("hybrid_app:teacher_list_view")





class BlockCreateView(CreateView):
    model = models.Block
    fields = "__all__"
    template_name = "hybrid_app/block_create_view.html"
    success_url = reverse_lazy("hybrid_app:block_create_view")





class TestView(TemplateView):
    template_name = "hybrid_app/test_view.html"
