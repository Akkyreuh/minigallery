from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_list, name='gallery_list'),
    path('add/', views.add_image, name='add_image'),
    path('upload/', views.upload_image, name='upload_image'),
    path('predict/', views.prediction_form, name='prediction_form'),
    path('predictions/', views.prediction_history, name='prediction_history'),
    path('api/images/', views.ImageListAPIView.as_view(), name='image-list-api'),
]