import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

key_vault_url = "https://azuresharekey.vault.azure.net/"
secret_name_connection_string = "AZURE-STORAGE-CONNECTION-STRING"
secret_name_container_name = "AZURE-STORAGE-CONTAINER-NAME"

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

connection_string_secret = secret_client.get_secret(secret_name_connection_string)
container_name_secret = secret_client.get_secret(secret_name_container_name)

AZURE_STORAGE_CONNECTION_STRING = connection_string_secret.value
AZURE_STORAGE_CONTAINER_NAME = container_name_secret.value

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
      #Following code just refreshes page if upload button clicked with no file attached.
      if f.filename == '':
        return render_template('index.html')
      #File is saved to 'saves' directory.
      else:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(file_path)

        blob_name = f.filename
        blob_client = container_client.get_blob_client(blob_name)

        #If file with same name already exists in blob storage, it is deleted first.
        blob = BlobClient.from_connection_string(conn_str=AZURE_STORAGE_CONNECTION_STRING, container_name=AZURE_STORAGE_CONTAINER_NAME, blob_name=blob_name)
        if blob.exists() == True:
          blob_client.delete_blob()
        
        #File is uploaded to blob storage.
        with open(file_path, 'rb') as data:
          blob_client.upload_blob(data)

        #Initial file removed from saves directory.
        os.remove(file_path)

        #Download URL is generated
        blob_client = container_client.get_blob_client(blob_name)
        url = blob_client.url

        #Upload successful template is rendered.
        return render_template('uploadsuccessful.html', link_url = url)

if __name__ == '__main__':
  app.run(debug=True)