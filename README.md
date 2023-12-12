# AzureShare

## Overview
AzureShare is a web application that allows you to upload and download files using Azure blob storage securely. The user selects a file via their file explorer to upload. A download link is then generated that can be copied and shared. Once clicked, the download link will download the file to the user's computer. 

This web application was developed using the Python Flask framework and is deployed on Azure app services. Using Azure SDK for Python, the uploaded file is automatically uploaded to Azure blob storage as a blob, and a download link is generated. Azure storage lifecycle management is used to automatically delete files 24 hours after creation to maintain security and cost efficiency.

![](https://github.com/drrohitpawar/AzureShare/blob/main/static/images/Demo.gif)

Azure Services used:
  - Azure App Services
  - Azure Blob Storage
  - Azure SDK for Python
  - Azure Storage Lifecycle Management
  - Azure Key Vaults
  

## Installation
If the web application is running, it can be accessed and used at the following link:
[azure-share.azurewebsites.net](azure-share.azurewebsites.net)

To run locally, clone to git repository to your own local machine:

```bash
$ git clone https://github.com/drrohitpawar/AzureShare.git
```

Once you are in the cloned directory in your terminal:

```bash
$ flask run
```

Then open a browser and connect to 'localhost:5000'

## Usage

1. Once the application is open, click on 'choose file' and browse file explorer for the file you want to upload.
2. Once selected, ensure you can see the correct file attached.
3. Click 'Upload' and wait for the successful upload screen to present.
4. You can now click on the 'copy' button to copy the download link to your clipboard and share with others.
5. Or you can click 'home' to return to homepage.
