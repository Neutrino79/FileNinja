import json

from django.shortcuts import render
import tempfile
from django.http import FileResponse, JsonResponse
from PyPDF2 import PdfFileMerger
import os
from django.views.decorators.csrf import csrf_exempt

import shutil

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