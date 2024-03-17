from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse


def pdf_to_docx(request):
    # Implement PDF to DOCX conversion logic here
    return JsonResponse({'message': 'PDF to DOCX conversion completed.'})


def pdf_to_ppt(request):
    # Implement PDF to PPT conversion logic here
    return JsonResponse({'message': 'PDF to PPT conversion completed.'})


def pdf_to_excel(request):
    # Implement PDF to Excel conversion logic here
    return JsonResponse({'message': 'PDF to Excel conversion completed.'})


def pdf_to_image(request):
    # Implement PDF to image conversion logic here
    return JsonResponse({'message': 'PDF to image conversion completed.'})
