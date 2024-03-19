import shutil
from wsgiref.util import FileWrapper

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
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse


@csrf_exempt
def pdf_to_docx(request):
    if request.method == 'POST':
        if request.FILES.get('pdf_file'):
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

                # Return the path to the converted DOCX file and the temporary directory
                return JsonResponse({'docx_path': docx_path, 'temp_dir': temp_dir})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'PDF file not provided.'}, status=400)
    else:
        # Render the HTML template
        return render(request, 'file_converter/pdf_to_docx.html')

def download_docx(request):
    if 'docx_path' in request.GET:
        docx_path = request.GET['docx_path']
        if os.path.exists(docx_path):  # Check if the file exists at the specified path
            # Open the file in binary mode
            try:
                with open(docx_path, 'rb') as f:
                    # Use FileResponse to serve the file
                    response = HttpResponse(f, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                    # Set the appropriate Content-Disposition header for downloading
                    response['Content-Disposition'] = 'attachment; filename="converted_file.docx"'
                    return response  # Serve the file
            except Exception as e:
                return HttpResponse("Error occurred while serving the file.", status=500)
        else:
            return HttpResponse("File not found.", status=404)  # Return HTTP 404 if the file is not found
    else:
        return HttpResponse("DOCX file path not provided.", status=400)  # Return HTTP 400 if the file path is not provided


def cleanup_temp_dir(request):
    if 'temp_dir' in request.GET:
        temp_dir = request.GET['temp_dir']
        try:
            # Clean up the temporary directory
            shutil.rmtree(temp_dir)

            # Check if the directory still exists after deletion
            if os.path.exists(temp_dir):
                print("Failed to delete temporary directory:", temp_dir)
            else:
                print("Temporary directory deleted successfully:", temp_dir)

            return HttpResponse("Temporary directory cleaned up successfully.")
        except Exception as e:
            return HttpResponse("Failed to clean up temporary directory: " + str(e), status=500)
    else:
        return HttpResponse("Temporary directory path not provided.", status=400)



def pdf_to_ppt(request):
    # Implement PDF to PPT conversion logic here
    return JsonResponse({'message': 'PDF to PPT conversion completed.'})


def pdf_to_excel(request):
    # Implement PDF to Excel conversion logic here
    return JsonResponse({'message': 'PDF to Excel conversion completed.'})


def pdf_to_image(request):
    # Implement PDF to image conversion logic here
    return JsonResponse({'message': 'PDF to image conversion completed.'})
