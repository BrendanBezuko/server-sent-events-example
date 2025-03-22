from django.urls import path
from . import views

urlpatterns = [
    path('sse/', views.sse_events, name='sse_events'),
    path('book/', views.create_booking, name='create_booking'),
]
