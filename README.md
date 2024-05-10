# S3-File-Manager

## *Overview:*

This project contains an implementation of a Python script for automating the process of moving specific files from one S3 folder to another based on a predefined prefix. The script also notifies a user via SNS (Simple Notification Service) when the file transfer operation is completed. The script is designed to handle errors gracefully and logs its operations for debugging purposes.

## *Script Functionality:*

1. List all objects in the `customer-details/` folder in an S3 bucket that start with the prefix `sr1_`.
2. Move each matching file to the `sr1/` folder within the same S3 bucket.
3. Delete the file from the source folder (`customer-details/`) after it has been copied to the destination folder (`sr1/`).
4. Log each operation, indicating which files have been moved and deleted.
5. Send a notification via SNS if at least one file has been moved.

## *Script Requirements:*

- The script is implemented in Python using the AWS SDK (Boto3) for interacting with AWS services.
- Error handling is implemented to gracefully handle scenarios such as no files to move and errors during file operations.
- Logging is utilized to record the details of each file operation for debugging and auditing purposes.
- SNS is used to send notifications to a specified topic when file transfer operations are completed.

## *Usage:*

1. Ensure Python and the AWS SDK (Boto3) are installed on the system.
2. Configure AWS credentials using `aws configure` or environment variables.
3. Create S3 bucket and a customer-details folder inside the bucket:
```bash
aws s3 mb s3://bucket-name
aws s3api put-object --bucket bucket-name --key customer-details/ --content-length 0
```
4. Add all the files in proj-files folder or any other sample files to the customer-details folder in the bucket:
```bash
aws s3 cp path/proj-files s3://bucket-name/customer-details --recursive
```
5. Check the contents of customer-details folder:
```bash
aws s3 ls s3://bucket-name/customer-details/
```
6. Create a SNS Topic, and an Email Subscription to the said topic:
```bash
aws sns create-topic --name topic-name
aws sns subscribe /
        --topic-arn topic-arn  /
        --protocol email  /
        --notification-endpoint example@example.com
```
7. Run the Python script `main.py` to execute the file transfer process.
8. Monitor the script output for status messages and errors.
9. Check the contents of both the customer-details/ and sr1/ folders.
10. Check your email for notifications regarding the file transfer operations.

## *Conclusion:*

The automated file transfer script provides a convenient solution for managing files within an S3 bucket. By automating the process of moving files based on predefined criteria and integrating with SNS for notifications, the script enhances efficiency and provides a streamlined workflow for file management tasks.
