from django.urls import path
from . import views

urlpatterns = [
    path('pdf_to_docx/', views.pdf_to_docx, name='pdf_to_docx'),
    path('download_docx/', views.download_docx, name='download_docx'),
    path('pdf_to_ppt/', views.pdf_to_ppt, name='pdf_to_ppt'),
    path('pdf_to_excel/', views.pdf_to_excel, name='pdf_to_excel'),
    path('pdf_to_image/', views.pdf_to_image, name='pdf_to_image'),
    path('cleanup_temp_dir/', views.cleanup_temp_dir, name='cleanup_temp_dir'),
]
