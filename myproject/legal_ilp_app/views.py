from django.shortcuts import render
from django.http import JsonResponse
import os
import subprocess
import glob
def upload_file(request):
    original_dir = os.getcwd()

    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.FILES['fileToUpload']
        file_name = uploaded_file.name
        print(file_name)
        # Write the uploaded file to 'data.txt'
        with open('C:\\Users\\mamid\\AppData\\Local\\Programs\\Python\\Python310\\chatbot - Copy\\myproject\\legal_ilp_app\\data\\data.txt', 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            data_file_length = os.path.getsize('C:\\Users\\mamid\\AppData\\Local\\Programs\\Python\\Python310\\chatbot - Copy\\myproject\\legal_ilp_app\\datas\\data.txt')
            length_file_path = 'C:\\Users\\mamid\\AppData\\Local\\Programs\\Python\\Python310\\chatbot - Copy\\myproject\\legal_ilp_app\\length_file.txt'
            # Append the data filename and its length to the length file
            
            formatted_data = '\t'.join(['data.txt', str(500)])
            with open(length_file_path, 'w') as length_file:
                length_file.write(formatted_data)
        # Run your scripts here
        data_path = 'C:\\Users\\mamid\\AppData\\Local\\Programs\\Python\\Python310\\chatbot - Copy\\myproject\\legal_ilp_app\\datas'
        prep_path = "prepared_data.json"
        summary_path = "summary/"
        os.chdir('legal_ilp_app')
        subprocess.run(["python", "prepareData.py", "--data_path", data_path, "--prep_path", prep_path])
        subprocess.run(["python", "legal_ilp.py", "--prep_path", "prepared_data.jsonprepared_data.json" , "--summary_path", summary_path, "--length_file", "length_file.txt", "--class_weights", "F=2", "I=3", "RLC=1", "A=1", "P=1", "S=1", "R=2", "RPC=3", "--default_sents", "1", "--content_weight", "1", "--legal_weight", "1", "--statute_weight", "2"])

        # Read the summarized content
       
        
        with open('C:\\Users\\mamid\\AppData\\Local\\Programs\\Python\\Python310\\chatbot - Copy\\myproject\\legal_ilp_app\\summary\\data.txt', 'r') as f:
            summary = f.read()
            print("summaryyyyyyyyyyyyyyyyyyyy",summary)
            os.chdir(original_dir)
            return JsonResponse({'summary': summary})
        

        # Return the summarized content as a JSON response
        

    return render(request, 'chat_ui.html')
def home(request):
    return render(request, 'home.html')