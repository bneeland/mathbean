from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter()
router.register('documents', views.DocumentViewSet, 'documents')
router.register('blocks', views.BlockViewSet, 'blocks')

app_name = 'hybrid_app'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/block-list/<int:pk>', views.BlockEditAPI.as_view()),
    path('', views.DocumentListView.as_view(), name='document_list_view'),
    path('<int:pk>', views.DocumentEditView.as_view(), name='document_edit_view'),
]
