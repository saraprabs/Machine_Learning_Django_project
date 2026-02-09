from django.urls import path

from core import views

urlpatterns = [
     path('predict/', views.predict_view, name='predict'),
]