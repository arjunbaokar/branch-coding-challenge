# branch-coding-challenge

- Read the gitignore to see the files you'll need to provide if you decide to pull it and run it

- Put AWS credentials into a file called 'aws_credentials', where the first line is AWS_ACCESS_KEY_ID, and the second is AWS_SECRET_ACCESS_KEY. Nothing else should be in the file. My file is not pushed to the repo, but make sure you add in aws_credentials or it won't be able to grab the data from AWS.

- I used RFs to figure out feature importance, and used that to feature select for the SVM. The SVM performed better overall, but that's because it's predicting the same value for everything. RF is performing roughly 3% above the baseline (86% as opposed to 83%), but it's actually predicting different values.

- Feature extraction is really slow: ~16min. It's the slowdown in reading the cursor from MongoDB though. This made the entire debugging process pretty slow. I adapted by writing features to a file once they were extracted, so each run wouldn't need to read features.

Time Distribution (total 6hrs):
~1.5 hours to set up AWS + Mongo, since it was my first time using either of them
~2.5 hours to get feature extraction up and working
~2 hours spent tuning models and trying to fix SVM