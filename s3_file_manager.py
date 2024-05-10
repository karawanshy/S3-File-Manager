import boto3
import logging

def move_s3_files():
    logging.basicConfig(filename='s3_file_move.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    s3_client = boto3.client('s3')
    sns_client = boto3.client('sns')
    
    bucket_name = 'bucket-name'
    source_folder = 'customer-details/'
    destination_folder = 'sr1/'
    prefix = 'sr1_'

    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=source_folder + prefix       # customer-details/sr1_
    )

    if 'Contents' not in response:
        logging.info("No files found to move.")
        return
    
    for obj in response['Contents']:
        key = obj['Key']

        try:
            # Moving the object to sr1/ folder
            s3_client.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': key},
                Key=destination_folder + key.split('/')[-1]     # move obj to sr1/ folder
            )

            # Deleting the obj from customer-details folder
            s3_client.delete_object(
                Bucket=bucket_name,
                Key=key
            )

            # Log the operation
            logging.info(f"Moved file {key} to {destination_folder} folder and deleted from {source_folder}.")

        except Exception as e:
                logging.error(f"An error occurred while copying/deleting file {key}: {str(e)}")

    try:
        sns_client.publish(
            TopicArn='topic-arn',
            Subject='S3 - File Move Notification',
            Message=f'Files have been moved to {destination_folder} folder and deleted from {source_folder}.'
        )

        logging.info('SNS notification sent.')
        
    except Exception as e:
            logging.error(f"An error occurred while sending SNS notification: {str(e)}")