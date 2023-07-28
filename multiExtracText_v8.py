import boto3
import json
import random
import logging
import concurrent.futures

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def extract_text(source_bucket, destination_bucket, document):
    # Create a new Textract client
    client = boto3.client('textract', region_name='ap-northeast-2')

    # Call Textract
    response = client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': source_bucket,
                'Name': document
            }
        })

    # Create a new S3 resource
    s3 = boto3.resource('s3')

    # Generate raw text
    raw_text = '\n'.join([block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE'])

    # Generate CSV text
    csv_text = '\n'.join([f"{block.get('Page', 'N/A')},LINE,{block['Text']},{block['Confidence']}" for block in response['Blocks'] if block['BlockType'] == 'LINE'])

    # Write each part to a separate object in the destination bucket
    s3.Object(destination_bucket, document + '-rawText.txt').put(Body=raw_text)
    s3.Object(destination_bucket, document + '-rawText.csv').put(Body=csv_text)
    s3.Object(destination_bucket, document + '-detectDocumentTextResponse.json').put(Body=json.dumps(response, indent=4))

def process_image(source_bucket, destination_bucket, item):
    # Create a new DynamoDB resource
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

    # Replace 'ProcessedObjects' with your DynamoDB table name
    table = dynamodb.Table('AwsTextractProcessedObjects')

    processed_item = table.get_item(Key={'Key': item['Key']})
    if 'Item' in processed_item:
        logger.info(f"Skipping {item['Key']} because it has already been processed.")
        return
    logger.info(f"Processing {item['Key']}...")
    extract_text(source_bucket, destination_bucket, item['Key'])

    # Write the key to the DynamoDB table
    table.put_item(Item={'Key': item['Key']})

def process_all_images(source_bucket, destination_bucket):
    # Create a new S3 client
    s3 = boto3.client('s3')

    # Create a paginator for the list_objects_v2 operation
    paginator = s3.get_paginator('list_objects_v2')

    # Initialize an empty list to hold all objects
    all_objects = []

    # Use the paginator to retrieve all objects
    for page in paginator.paginate(Bucket=source_bucket):
        all_objects.extend(page['Contents'])

    # Shuffle the list of objects
    random.shuffle(all_objects)

    # Process each object in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda item: process_image(source_bucket, destination_bucket, item), all_objects)

# Replace 'source-bucket' and 'destination-bucket' with your bucket names
process_all_images('winegraph-wine-labels', 'winegraph-wine-labels-textract-outputs')
