import os
import boto
import json
from pymongo import MongoClient

class DataManager:

	def __init__(self):
		self.client = MongoClient()
		self.set_credentials()

		self.db = self.client.branch_challenge
		self.s3_conn = boto.connect_s3()
		self.bucket = self.s3_conn.get_bucket('branch-test-warehouse')

	# Sets AWS credentials so it can read stuff
	def set_credentials(self):
		with open('aws_credentials') as f:
			os.environ['AWS_ACCESS_KEY_ID'] = f.readline().strip()
			os.environ['AWS_SECRET_ACCESS_KEY'] = f.readline().strip()

	# Call this after instantiating DataManager object to populate the DB.
	def populate_db(self):
		user_data_keys = self.bucket.get_all_keys(prefix='uploads/users')

		for key in user_data_keys:
			key_split = filter(None, key.name.split('/'))
			if len(key_split) > 5:
				user_id = key_split[2]
				key_type = key_split[4]

				contents = key.get_contents_as_string()
				contents = json.loads(contents)
				for d in contents:
					d['uid'] = user_id
					d['key_type'] = key_type

				try:
					db_result = self.db.test.insert_many(contents)
				except:
					print "Empty: ", key_split

dm = DataManager()
dm.populate_db()