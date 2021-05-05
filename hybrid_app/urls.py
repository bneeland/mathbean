from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter()
router.register('documents', views.DocumentViewSet, 'documents')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.DocumentListView.as_view(), name='document_list'),
    path('<int:pk>', views.DocumentEditorView.as_view(), name='document_editor_view'),
    path('session', views.SessionView.as_view(), name='session_view'),
    path('editor', views.EditorView.as_view(), name='editor_view'),
]
