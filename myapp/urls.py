from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from .views import InventoreyView, HandledErrorView, UnHandledErrorView

def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('checkout', InventoreyView.as_view()),
    path('handled', HandledErrorView.as_view()),
    path('unhandled', UnHandledErrorView.as_view()),
    path('sentry-debug/', trigger_error),

]
