# branch-coding-challenge

- Read the gitignore to see the files you'll need to provide if you decide to pull it and run it

- Put AWS credentials into a file called 'aws_credentials', where the first line is AWS_ACCESS_KEY_ID, and the second is AWS_SECRET_ACCESS_KEY. Nothing else should be in the file. My file is not pushed to the repo, but make sure you add in aws_credentials or it won't be able to grab the data from AWS.

- I used RFs to figure out feature importance, and used that to feature select for the SVM. The SVM performed better overall, but that's because it's predicting the same value for everything. RF is performing roughly 3% above the baseline (86% as opposed to 83%), but it's actually predicting different values.

- Feature extraction is really slow: ~16min. It's the slowdown in reading the cursor from MongoDB though. I tried adapting batch_sizes, but that's not the problem. The slowdown is purely from the iteration, and not the computation within the cursor iteration, though. I've tested that.
Overall, This made the entire debugging process pretty slow. I adapted by writing features to a file once they were extracted, so each run wouldn't need to re-read features. This resulted in a lot of wasted time, though.


Time Distribution (total 6.5 hours):
~1 hours planning the system, understanding data and stuff
~1.5 hours to set up AWS + Mongo, since it was my first time using either of them
~3 hours to get feature extraction up and working, given that it took forever for each run
~1 hours spent tuning models and trying to fix SVM

Given more time:
I'd look for better features, since that's what is probably causing all of the issues with the model.
I'd make feature extraction faster so I could test features faster. That's the main bottleneck.