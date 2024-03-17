from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from docx import Document
from pdf2docx import Converter
import tempfile
import os


def pdf_to_docx(request):
    # Implement PDF to DOCX conversion logic here
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']

        # Create a temporary directory to store intermediate files
        temp_dir = tempfile.mkdtemp()

        # Save the uploaded PDF file to the temporary directory
        pdf_path = os.path.join(temp_dir, pdf_file.name)
        with open(pdf_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # Define docx_path with a default value
        docx_path = ''

        # Convert PDF to DOCX
        try:
            # Use pdf2docx library to convert PDF to DOCX
            docx_path = os.path.join(temp_dir, 'output.docx')
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()

            # Return the converted DOCX file
            with open(docx_path, 'rb') as docx_file:
                response = HttpResponse(docx_file.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = f'attachment; filename="{pdf_file.name.replace(".pdf", ".docx")}"'
                return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            # Clean up temporary directory
            os.unlink(pdf_path)
            if docx_path:
                os.unlink(docx_path)
            os.rmdir(temp_dir)
    else:
        return JsonResponse({'error': 'PDF file not provided.'}, status=400)


def pdf_to_ppt(request):
    # Implement PDF to PPT conversion logic here
    return JsonResponse({'message': 'PDF to PPT conversion completed.'})


def pdf_to_excel(request):
    # Implement PDF to Excel conversion logic here
    return JsonResponse({'message': 'PDF to Excel conversion completed.'})


def pdf_to_image(request):
    # Implement PDF to image conversion logic here
    return JsonResponse({'message': 'PDF to image conversion completed.'})
