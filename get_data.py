import os
import boto
from pymongo import MongoClient

with open('aws_credentials') as f:
	os.environ['AWS_ACCESS_KEY_ID'] = f.readline().strip()
	os.environ['AWS_SECRET_ACCESS_KEY'] = f.readline().strip()


# client = MongoClient()
# db = client.branchtest

s3_conn = boto.connect_s3()
bucket = s3_conn.get_bucket('branch-test-warehouse')
rs = s3_conn.get_all_buckets()
for b in rs:
	print b.name