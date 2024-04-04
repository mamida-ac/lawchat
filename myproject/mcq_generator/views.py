from django.shortcuts import render
import json

def mcq_generator(request):
    json_file_path = 'mcq_generator/ipc.json'

    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        ipc_data = json.load(file)
        ipcdata = json.dumps(ipc_data)
    # Pass the JSON data to the template
    return render(request, 'mcq_input.html', {'ipc_data': ipcdata})
