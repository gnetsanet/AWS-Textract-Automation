# AWS Textract Automation

This repository contains a Python script for automating the process of extracting text from images using AWS Textract. The script processes images stored in an S3 bucket, extracts text from each image using Textract, and stores the extracted text in another S3 bucket. The script also keeps track of which images have been processed in a DynamoDB table to avoid processing the same image multiple times.

## Features

- **Automated text extraction**: The script automatically extracts text from images using AWS Textract, a service that uses machine learning to extract text from documents.

- **Parallel processing**: The script uses multithreading to process multiple images in parallel, which can significantly speed up the text extraction process.

- **Error handling and logging**: The script includes error handling to gracefully handle any issues that arise during the text extraction process. It also includes logging to provide visibility into the process.

- **DynamoDB integration**: The script uses a DynamoDB table to keep track of which images have been processed. This allows the script to skip over images that have already been processed, saving time and resources.

## Usage

To use the script, you'll need to have AWS credentials set up on your machine. You'll also need to replace `'source-bucket'` and `'destination-bucket'` with the names of your source and destination S3 buckets, respectively. You'll also need to replace `'AwsTextractProcessedObjects'` with the name of your DynamoDB table.

Once you've set up your AWS credentials and updated the bucket and table names, you can run the script with the following command:

```bash
python3 multiExtracText_v8.py
```

Replace `multiExtracText_v8.py` with the name of the Python script.

## Future Work

There are several potential improvements that could be made to this script:

- **Increase parallelism**: The script currently uses a fixed number of worker threads. This could be increased or made configurable to take better advantage of multi-core machines.

- **Use multiprocessing**: The script currently uses multithreading, which can be limited by Python's Global Interpreter Lock (GIL). Switching to multiprocessing could potentially achieve greater speedup.

- **Optimize AWS usage**: The script could potentially be optimized to make fewer requests to AWS services, use batch operations, or use provisioned throughput to increase capacity.

- **Use a faster programming language or library**: If the speed of the Python interpreter is a bottleneck, the script could potentially be rewritten in a faster programming language or use a faster Python library.

Please note that these improvements would involve trade-offs and would require careful consideration and testing.
