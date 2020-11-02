from flask import Flask, render_template, request
import os
import yaml
from azure.storage.blob import ContainerClient

app = Flask(__name__)

def get_files(dir):
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file() and not entry.name.startswith('.'):
                yield entry

def upload(files, connection_string, container_name):
    container_client = ContainerClient.from_connection_string(connection_string, container_name)
    print("Uploading....")

    for file in files:
        blob_client = container_client.get_blob_client(file.name)
        with open(file.path, "rb") as data:
            blob_client.upload_blob(data)
            print(f'{file.name} uploaded to blob storage')
            os.remove(file)
            print(f'{file.name} removed from folder')


@app.route('/', methods=['POST', 'GET'])
def index():
    azure_storage_connectionstring = ""
    mp3_container_name =  "mp3"
    source_folder = "/Users/lawnce/Desktop/fma/data/fma_test"

    if request.method == 'POST':
        files = get_files(source_folder)
        upload(files, azure_storage_connectionstring, mp3_container_name)
        return 'Successfull transferred to blob'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
