from django.urls import path
from . import views

urlpatterns = [
    path('cleanup/', views.cleanup, name='cleanup'),
    path('pdf_merge/', views.pdf_merge, name='pdf_merge'),

]