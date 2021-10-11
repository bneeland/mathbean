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
    path('student-lists/create', views.CreateStudentListView.as_view(), name='create_student_list_view'),
    path('student-lists/<int:pk>/update', views.UpdateStudentListView.as_view(), name='update_student_list_view'),
    path('students', views.StudentListView.as_view(), name='student_list_view'),
    path('students/create', views.CreateStudentView.as_view(), name='create_student_view'),
    path('students/<int:pk>/update', views.UpdateStudentView.as_view(), name='update_student_view'),
    path('students/<int:pk>/delete', views.DeleteStudentView.as_view(), name='delete_student_view'),
    path('teachers', views.TeacherListView.as_view(), name='teacher_list_view'),
    path('teachers/create', views.CreateTeacherView.as_view(), name='create_teacher_view'),
    path('teachers/<int:pk>/update', views.UpdateTeacherView.as_view(), name='update_teacher_view'),
    path('teachers/<int:pk>/delete', views.DeleteTeacherView.as_view(), name='delete_teacher_view'),
    path('create-document', views.CreateDocumentView.as_view(), name='create_document_view'),
    path('block-create-view', views.BlockCreateView.as_view(), name='block_create_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
