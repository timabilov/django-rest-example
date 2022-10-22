from django.urls import path
from .views import TestDetailsAPIView


urlpatterns = (
    path('test/<str:code>', TestDetailsAPIView.as_view()),
)
