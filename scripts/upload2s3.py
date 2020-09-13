#!/usr/bin/env python3

import boto3 
from botocore.exceptions import NoCredentialsError
from json import loads
from datetime import datetime

filename = str(datetime.now()) + 'practice'

passfile = open('./../data/words', 'r')
words = loads(passfile.read())
ACCESS_KEY = words['access'] 
SECRET_KEY = words['secret']
region = words['region']
passfile.close()

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

upload_successful = upload_to_aws('./../data/practice', 'sensor-dht22', 'practice/{}'.format(filename))