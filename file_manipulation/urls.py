from django.urls import path
from . import views

urlpatterns = [
    path('cleanup/', views.cleanup, name='cleanup'),
    path('pdf_merge/', views.pdf_merge, name='pdf_merge'),
    path('pdf_split/', views.pdf_split, name='pdf_split'),
    path('pdf_compress/', views.pdf_compress, name='pdf_compress'),

]