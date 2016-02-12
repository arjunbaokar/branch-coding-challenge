import os
import boto
import json
import numpy as np
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
		for key in self.bucket.list(prefix='uploads/users'):
			key_split = filter(None, key.name.split('/'))
			if len(key_split) > 5:
				user_id = int(key_split[2])
				key_type = key_split[4]
				device_type = 0 if key_split is 'unknown' else 1

				contents = key.get_contents_as_string()
				try:
					contents = json.loads(contents)
				except:
					print "JSON parse failed: ", key_split
					continue

				for d in contents:
					d['uid'] = user_id
					d['key_type'] = key_type
					d['device_type'] = device_type

				try:
					db_result = self.db.test.insert_many(contents)
				except:
					print "Empty: ", key_split

				if user_id % 1000 == 0:
					print "Reached ", user_id

	# Returns a numpy 2-D array of features where each row is the features for a given user
	def generate_features(self):
		fts = []
		max_uid = self.db.test.find_one(sort=[('uid', -1)])['uid']

		for uid in range(max_uid+1):
			call_log = self.db.test.find({'uid': uid, 'key_type': 'call_log'})
			print self.call_log_features(call_log)

			sms_log = self.db.test.find({'uid': uid, 'key_type': 'sms_log'})
			contact_list = self.db.test.find({'uid': uid, 'key_type': 'contact_list'})

			# break # FIXME: remove me

	# Generates call log features for single user
	def call_log_features(self, user_data):
		calls_per_quarter_day = [0, 0, 0, 0]
		total_duration = 0
		ONE_DAY = 24*60*60*1000
		QUARTER_DAY = ONE_DAY/4

		for item in user_data:
			time_of_day = item['datetime'] % ONE_DAY
			calls_per_quarter_day[time_of_day/QUARTER_DAY] += 1
			total_duration += item['duration']

		return calls_per_quarter_day + [total_duration]

	# Generates sms features for single user
	def sms_log_features(self, user_data):
		return

	# Generates contacts features for single user
	def contact_list_features(self, user_data):
		return

	# Return a numpy array of labels {0,1}^K, where K is the number of users.
	# 0 if bad (delinquent) borrower, 1 if good borrower. Labels are determined from delinquent borrower list.
	def generate_labels(self, fts):
		delinquent_users = set()
		labels = []
		with open('delinquent_borrowers_10.txt') as f:
			for line in f:
				if len(line) > 1:
					uid_string = 'User id: '
					start = line.index(uid_string) + len(uid_string)-1
					end = line.index(',', start)
					delinquent_users.add( int(line[start:end]) )

		for i in range(len(fts)):
			if fts[i][0] in delinquent_users:
				labels.append(0)
			else:
				labels.append(0)

		return np.array(labels)




dm = DataManager()
# dm.populate_db()
dm.generate_features()
# dm.generate_labels()