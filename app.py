import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=azuresharestorage1;AccountKey=zoVBbbdCL90orOAUR4XArWDgSZYSEKUtSnOS8+/cssuDnfF4qVCEqryuTlvjwDm2/GChNH2KTxA4+AStFKknTQ==;EndpointSuffix=core.windows.net"
AZURE_STORAGE_CONTAINER_NAME = "azureshare"

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'saves')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
      f.save(file_path)

      blob_name = f.filename
      blob_client = container_client.get_blob_client(blob_name)
      with open(file_path, 'rb') as data:
        blob_client.upload_blob(data)

      os.remove(file_path)

      return render_template('uploadsuccessful.html')

if __name__ == '__main__':
  app.run(debug=True)