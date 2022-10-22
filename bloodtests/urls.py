from django.urls import path
from .views import TestDetails


urlpatterns = (
    path('test/<str:code>', TestDetails.as_view()),
)
