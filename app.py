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
      if f.filename == '':
        return render_template('index.html')
      else:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(file_path)

        blob_name = f.filename
        blob_client = container_client.get_blob_client(blob_name)

        blob = BlobClient.from_connection_string(conn_str=AZURE_STORAGE_CONNECTION_STRING, container_name=AZURE_STORAGE_CONTAINER_NAME, blob_name=blob_name)
        if blob.exists() == True:
          blob_client.delete_blob()
        
        with open(file_path, 'rb') as data:
          blob_client.upload_blob(data)

        os.remove(file_path)

        blob_client = container_client.get_blob_client(blob_name)
        url = blob_client.url

        return render_template('uploadsuccessful.html', link_url = url)

if __name__ == '__main__':
  app.run(debug=True)