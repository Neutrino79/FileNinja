import json
from django.shortcuts import render
import tempfile
from django.http import FileResponse, JsonResponse, HttpResponse
from PyPDF2 import PdfFileMerger
import os
from django.views.decorators.csrf import csrf_exempt
import shutil
from PyPDF2 import PdfFileReader
from zipfile import ZipFile
from PyPDF2 import PdfFileWriter
import subprocess



@csrf_exempt
def cleanup(request):
    if request.method == 'POST':
        # Load the temp_dir from the request
        temp_dir = json.loads(request.body)['temp_dir']
        print("deleting temp dir: ", temp_dir)
        # Delete the temporary directory
        shutil.rmtree(temp_dir)

        print('Temporary directory deleted.')
        return JsonResponse({'message': 'Temporary directory deleted.'})
    else:
        print("Temp dir not deleted")
        return JsonResponse({'message': 'Temporary directory not deleted.'})


@csrf_exempt
def pdf_merge(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files[]')
        merger = PdfFileMerger()
        temp_dir = tempfile.mkdtemp(dir='/private/var/folders/h2/59vhr73s5t55sgq10fd9m8sc0000gn/T/File_Ninja_Temp')

        for uploaded_file in uploaded_files:
            temp_file_path = os.path.join(temp_dir, uploaded_file.name)

            with open(temp_file_path, 'wb') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            merger.append(temp_file_path)

        output_filename = os.path.join(temp_dir, 'merged.pdf')
        merger.write(output_filename)
        merger.close()

        file = open(output_filename, 'rb')
        response = FileResponse(file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
        response['temp_dir'] = temp_dir
        return response
    else:
        return render(request, 'file_manipulation/pdf_merge.html')


@csrf_exempt
def pdf_split(request):
    if request.method == 'POST':
        # Get the uploaded file, split option, and page ranges from the POST data
        uploaded_file = request.FILES['file']
        split_option = request.POST['splitOption']
        page_ranges = json.loads(request.POST['pageRanges'])

        # Create a PdfFileReader object from the uploaded file
        pdf = PdfFileReader(uploaded_file)
        total_pages = pdf.getNumPages()
        for start, end in page_ranges:
            if start < 1 or end > total_pages:
                return JsonResponse({'error': 'Page range is outside the total number of pages.'}, status=400)
        # Create a temporary directory to store the split PDF files
        temp_dir = tempfile.mkdtemp(dir='/private/var/folders/h2/59vhr73s5t55sgq10fd9m8sc0000gn/T/File_Ninja_Temp')

        # Split the PDF file according to the split option and page ranges
        if split_option == 'every-page':
            for i in range(pdf.getNumPages()):
                writer = PdfFileWriter()
                writer.addPage(pdf.getPage(i))
                with open(os.path.join(temp_dir, f'page_{i+1}.pdf'), 'wb') as output_pdf:
                    writer.write(output_pdf)
        elif split_option == 'range':
            for start, end in page_ranges:
                writer = PdfFileWriter()
                for i in range(start-1, end):
                    writer.addPage(pdf.getPage(i))
                with open(os.path.join(temp_dir, f'pages_{start}_to_{end}.pdf'), 'wb') as output_pdf:
                    writer.write(output_pdf)

        # Create a zip file from the split PDF files
        zip_filename = os.path.join(temp_dir, 'split_pdf.zip')
        print("zip_filename: ", zip_filename)
        with ZipFile(zip_filename, 'w') as zip_file:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.pdf'):
                        zip_file.write(os.path.join(root, file), arcname=file)

        # Send the zip file as a response to the browser
        with open(zip_filename, 'rb') as zip_file:
            response = HttpResponse(zip_file, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="split_pdf.zip"'
            response['temp_dir'] = temp_dir
            return response

    else:
        return render(request, 'file_manipulation/pdf_split.html')


@csrf_exempt
def pdf_compress(request):
    compressed_sizes = {}
    if request.method == 'POST':
        # Get the uploaded files and the compression value from the POST data
        uploaded_files = request.FILES.getlist('pdf_file')
        compression_value = request.POST['compression_value']


        # Create a temporary directory to store the compressed PDF file
        temp_dir = tempfile.mkdtemp(dir='/private/var/folders/h2/59vhr73s5t55sgq10fd9m8sc0000gn/T/File_Ninja_Temp')

        # Map the compression value to a quality setting for Ghostscript
        quality_settings = {
            '100': 'default',
            '75': 'printer',
            '50': 'ebook',
            '25': 'screen'
        }
        quality = quality_settings.get(compression_value, 'default')

        for uploaded_file in uploaded_files:
            input_filename = os.path.join(temp_dir, uploaded_file.name)
            output_filename = os.path.join(temp_dir, 'compressed_' + uploaded_file.name)

            # Save the uploaded file to the temporary directory
            with open(input_filename, 'wb') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            # Compress the PDF file using Ghostscript
            subprocess.call([
                'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                '-dPDFSETTINGS=/' + quality, '-dNOPAUSE', '-dQUIET', '-dBATCH',
                '-sOutputFile=' + output_filename,
                input_filename
            ])

            compressed_size = os.path.getsize(output_filename)
            compressed_sizes[uploaded_file.name] = compressed_size

        # Create a zip file from the compressed PDF files
        zip_filename = os.path.join(temp_dir, 'compressed_files.zip')
        with ZipFile(zip_filename, 'w') as zip_file:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.startswith('compressed_'):
                        zip_file.write(os.path.join(root, file), arcname=file)

        # Send the zip file as a response to the browser
        compressed_sizes_json = json.dumps(compressed_sizes)
        print("compressed_sizes_json: ", compressed_sizes_json)
        with open(zip_filename, 'rb') as zip_file:
            response = HttpResponse(zip_file, content_type='application/zip')
            response['X-Compressed-Sizes'] = compressed_sizes_json
            response['Content-Disposition'] = 'attachment; filename="compressed_files.zip"'
            response['temp_dir'] = temp_dir
            print("temp_dir: ", temp_dir)
            return response

    else:
        return render(request, 'file_manipulation/pdf_compress.html')