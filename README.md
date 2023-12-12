# AzureShare

## Overview
AzureShare is a web application that allows you to upload and download files using Azure blob storage securely. The user selects a file via their file explorer to upload. A download link is then generated that can be copied and shared. Once clicked, the download link will download the file to the user's computer. 

This web application was developed using the Python Flask framework and is deployed on Azure app services. Using Azure SDK for Python, the uploaded file is automatically uploaded to Azure blob storage as a blob, and a download link is generated. Azure storage lifecycle management is used to automatically delete files 24 hours after creation to maintain security and cost efficiency.
