from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def pdf_merge(request):
    return render(request, 'file_manipulation/pdf_merge.html')

