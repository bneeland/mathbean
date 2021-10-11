from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('documents', views.DocumentViewSet, 'documents')
router.register('blocks', views.BlockViewSet, 'blocks')

app_name = 'hybrid_app'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/block-edit/<int:pk>', views.BlockEditAPI.as_view()),
    path('api/move-block/<direction>/<int:document_pk>/<int:pk>', views.MoveBlockAPI.as_view()),
    path('api/delete-block/<int:document_pk>/<int:pk>', views.DeleteBlockAPI.as_view()),
    path('', views.HomeView.as_view(), name='home_view'),
    path('documents/', views.DocumentListView.as_view(), name='document_list_view'),
    path('documents/<int:pk>', views.DocumentEditView.as_view(), name='document_edit_view'),
    path('documents/<int:pk>/share', views.DocumentShareView.as_view(), name='document_share_view'),
    path('documents/<int:pk>/delete', views.DocumentDeleteView.as_view(), name='document_delete_view'),
    path('student-lists', views.StudentListListView.as_view(), name='student_list_list_view'),
    path('student-lists/create', views.StudentListCreateView.as_view(), name='student_list_create_view'),
    path('student-lists/<int:pk>/update', views.StudentListUpdateView.as_view(), name='student_list_update_view'),
    path('students', views.StudentListView.as_view(), name='student_list_view'),
    path('students/create', views.StudentCreateView.as_view(), name='student_create_view'),
    path('students/<int:pk>/update', views.StudentUpdateView.as_view(), name='student_update_view'),
    path('students/<int:pk>/delete', views.StudentDeleteView.as_view(), name='student_delete_view'),
    path('teachers', views.TeacherListView.as_view(), name='teacher_list_view'),
    path('teachers/create', views.TeacherCreateView.as_view(), name='teacher_create_view'),
    path('teachers/<int:pk>/update', views.TeacherUpdateView.as_view(), name='teacher_update_view'),
    path('teachers/<int:pk>/delete', views.DeleteTeacherView.as_view(), name='delete_teacher_view'),
    path('create-document', views.DocumentCreateView.as_view(), name='document_create_view'),
    path('block-create-view', views.BlockCreateView.as_view(), name='block_create_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
