from django.urls import path
from . import views

urlpatterns = [
    path('pdf_to_docx/', views.pdf_to_docx, name='pdf_to_docx'),
    path('pdf_to_ppt/', views.pdf_to_ppt, name='pdf_to_ppt'),
    path('pdf_to_excel/', views.pdf_to_excel, name='pdf_to_excel'),
    path('pdf_to_image/', views.pdf_to_image, name='pdf_to_image'),
]
