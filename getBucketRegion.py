#!/usr/bin/env python3
import boto3
import subprocess
import sys
import argparse
import logging

bucket_name = "nw-testsync2"
client = boto3.client('s3')
# result = client.Bucket(bucket_name)
# print result

response = client.get_bucket_location(
    Bucket=bucket_name
)


print(response["LocationConstraint"])

print(response)
# s3 = boto3.resource('s3')
# bucket = s3.Bucket(bucket_name)
# print(bucket)