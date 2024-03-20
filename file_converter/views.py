import shutil
from wsgiref.util import FileWrapper

import pdf2pptx
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from docx import Document
from pdf2docx import Converter
from pdf2pptx import convert_pdf2pptx
from PIL import Image
from fpdf import FPDF
import base64
import io
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
            temp_dir = tempfile.mkdtemp(dir='/private/var/folders/h2/59vhr73s5t55sgq10fd9m8sc0000gn/T/File_Ninja_Temp')

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


def download_file(request):
    if 'file_path' in request.GET:
        file_path = request.GET['file_path']
        if os.path.exists(file_path):  # Check if the file exists at the specified path
            # Open the file in binary mode
            try:
                with open(file_path, 'rb') as f:
                    if file_path.endswith('.docx'):
                        content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                    elif file_path.endswith('.pptx'):
                        content_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
                    elif file_path.endswith('.pdf'):
                        content_type = 'application/pdf'
                    else:
                        return HttpResponse("Unsupported file format.", status=400)

                        # Use FileResponse to serve the file
                    response = HttpResponse(f, content_type=content_type)
                    # Set the appropriate Content-Disposition header for downloading
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
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

@csrf_exempt
def pdf_to_ppt(request):
    if request.method == 'POST':
        if request.FILES.get('pdf_file'):
            pdf_file = request.FILES['pdf_file']

            # Create a temporary directory to store intermediate files
            temp_dir = tempfile.mkdtemp(dir='/private/var/folders/h2/59vhr73s5t55sgq10fd9m8sc0000gn/T/File_Ninja_Temp')

            # Save the uploaded PDF file to the temporary directory
            pdf_path = os.path.join(temp_dir, pdf_file.name)
            with open(pdf_path, 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            # Define pptx_path with a default value
            pptx_path = ''

            # Convert PDF to PPTX
            try:
                # Define the output path for the PPTX file
                pptx_path = os.path.join(temp_dir, 'output.pptx')

                # Convert PDF to PPTX
                convert_pdf2pptx(pdf_path, pptx_path, resolution=300, start_page=0, page_count=None)

                # Return the path to the converted PPTX file and the temporary directory
                return JsonResponse({'pptx_path': pptx_path, 'temp_dir': temp_dir})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'PDF file not provided.'}, status=400)
    else:
        # Render the HTML template
        return render(request, 'file_converter/pdf_to_ppt.html')


def pdf_to_excel(request):
    # Implement PDF to Excel conversion logic here
    return JsonResponse({'message': 'PDF to excel conversion completed.'})


def pdf_to_image(request):
    # Implement PDF to image conversion logic here
    return JsonResponse({'message': 'PDF to image conversion completed.'})



import json
import img2pdf

@csrf_exempt
def img_to_pdf(request):
    print("POST keys:", request.POST.keys())
    if request.method == 'POST':
        images = json.loads(request.POST.get('images'))
        if images:
            # Create a temporary directory to store the PDF file
            temp_dir = tempfile.mkdtemp(dir='/private/var/folders/h2/59vhr73s5t55sgq10fd9m8sc0000gn/T/File_Ninja_Temp')

            # Define the path for the PDF file
            pdf_path = os.path.join(temp_dir, 'output.pdf')

            # Create a list to store the image data
            img_data_list = []

            # Define the size of an A4 paper in pixels (at 300 DPI)
            a4_size = (2480, 3508)

            # Loop through the images
            for image in images:
                try:
                    # Decode the base64 image
                    img_data = base64.b64decode(image['src'].split(',')[1])
                    img = Image.open(io.BytesIO(img_data))

                    # Rotate the image
                    img = img.rotate(-image['angle'])

                    # Calculate the aspect ratio of the image and the A4 paper
                    img_aspect = img.width / img.height
                    a4_aspect = a4_size[0] / a4_size[1]

                    # Resize the image to fit within the size of an A4 paper, maintaining aspect ratio
                    if img_aspect > a4_aspect:
                        # If the image is wider, set the width to the width of the A4 paper
                        img = img.resize((a4_size[0], round(a4_size[0] / img_aspect)))
                    else:
                        # If the image is taller, set the height to the height of the A4 paper
                        img = img.resize((round(a4_size[1] * img_aspect), a4_size[1]))

                    # Create a new blank image with a white background and the size of an A4 paper
                    a4_img = Image.new('RGB', a4_size, 'white')

                    # Calculate the position to paste the image onto the blank image
                    # This will center the image
                    pos = ((a4_size[0] - img.width) // 2, (a4_size[1] - img.height) // 2)

                    # Paste the image onto the blank image
                    a4_img.paste(img, pos)

                    # Save the image to a temporary file
                    img_path = os.path.join(temp_dir, 'temp.png')
                    a4_img.save(img_path)

                    # Add the image data to the list
                    img_data_list.append(open(img_path, 'rb').read())
                except Exception as e:
                    print(f"Error processing image: {e}")

            # Convert the images to PDF
            with open(pdf_path, "wb") as f:
                f.write(img2pdf.convert(img_data_list))

            # Return the path to the PDF file
            return JsonResponse({'pdf_path': pdf_path, 'temp_dir': temp_dir})
        else:
            return JsonResponse({'error': 'Images not provided.'}, status=400)
    else:
        return render(request, 'file_converter/img_to_pdf.html')