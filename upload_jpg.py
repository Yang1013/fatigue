import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

def run_sample():
   # Create the BlockBlockService that is used to call the Blob service for the storage account
   block_blob_service = BlockBlobService(account_name='no662', account_key='k8xm7XDmHTpkc9VLa9ZISxHoWpDfLgTspAHdwpjSckOI546AoopE17lKUDlVeaqD+GAz7FN+uh1M9/B7eEDgzg==')
   
   for root, dir, files in os.walk("./"):
      for file in files:
         if file.endswith(".jpg") and file.startswith("unknown"):  
            block_blob_service.create_blob_from_path("data2", file , "/home/joey/Desktop/fatigue-master/" + file)
        
# Main method.
if __name__ == '__main__':
    run_sample()