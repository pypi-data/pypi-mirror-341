import boto3
import os
# method to read the pt file from a file path and save into an s3 bucket
def persist_model(message_type, experiment_name, file_path):
    # Hardcoded S3 bucket name
    bucket_name = 'neuroedge-device'

    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Check if message type is 1
    if message_type == 1:
        # Check if the file exists
        if os.path.exists(file_path):
            try:
                # Generate an S3 object key by concatenating the experiment name and the base name of the file with an underscore 
                s3_key = f'{experiment_name}_{os.path.basename(file_path)}'
                
                # Upload file to S3
                s3.upload_file(file_path, bucket_name, s3_key)
                print(f"File '{file_path}' successfully uploaded to '{bucket_name}/{s3_key}'")
            except Exception as e:
                print(f"Error uploading file to S3: {e}")
        else:
            print(f"File '{file_path}' does not exist.")
    else:
        print("Message type is not 1, no upload performed.")