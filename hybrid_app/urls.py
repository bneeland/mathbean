from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter()
router.register('documents', views.DocumentViewSet, 'documents')
router.register('blocks', views.BlockViewSet, 'blocks')

app_name = 'hybrid_app'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/block-edit/<int:pk>', views.BlockEditAPI.as_view()),
    path('', views.DocumentListView.as_view(), name='document_list_view'),
    path('create-document', views.CreateDocumentView.as_view(), name='create_document_view'),
    path('<int:pk>', views.DocumentEditView.as_view(), name='document_edit_view'),
    path('block-create-view', views.BlockCreateView.as_view(), name='block_create_view'),
    path('test-view', views.TestView.as_view(), name="test_view"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
