#### This code is used for loading a subset of data from 57 GB files, and saving it to training.csv and validation.csv


!wget -O "val.tsv" "https://elasticbeanstalk-us-west-2-800068098556.s3.amazonaws.com/challenge-website/public_data/val.tsv?AWSAccessKeyId=AKIA3UR6GLH6F73MJVWF&Signature=g8XsxhImMPtroU8pwXsVn3ypfoE%3D&Expires=1590223628"

!wget -O "train.tsv" "https://elasticbeanstalk-us-west-2-800068098556.s3.amazonaws.com/challenge-website/public_data/training.tsv?AWSAccessKeyId=AKIA3UR6GLH6F73MJVWF&Signature=zmSd6rA4RT%2Biw8QDyhF0ynTGgMw%3D&Expires=1590241904"
drive.flush_and_unmount()


#### Line 8 to Line 18 have been taken from http://www.recsyschallenge.com/2020/, as the code was made available to all particpant for loading the data
all_features = ["text_ tokens", "hashtags", "tweet_id", "present_media", "present_links", "present_domains",\
                "tweet_type","language", "tweet_timestamp", "engaged_with_user_id", "engaged_with_user_follower_count",\
               "engaged_with_user_following_count", "engaged_with_user_is_verified", "engaged_with_user_account_creation",\
               "engaging_user_id", "engaging_user_follower_count", "engaging_user_following_count", "engaging_user_is_verified",\
               "engaging_user_account_creation", "engagee_follows_engager"]

all_features_to_idx = dict(zip(all_features, range(len(all_features))))
labels_to_idx = {"reply_timestamp": 20, "retweet_timestamp": 21, "retweet_with_comment_timestamp": 22, "like_timestamp": 23}
t_set = []
v_set = []
cou = 0

with open("Copy of train.tsv", encoding="utf-8") as f:
    line = f.readline()
    while line:
        line = line.strip()
        features = line.split("\x01")
        # for feature, idx in all_features_to_idx.items():
            # print("feature {} has value {}".format(feature, features[idx]))

        # for label, idx in labels_to_idx.items():
        #     print("label {} has value {}".format(label, features[idx]))
    
        if cou%100000==0:
            print("counter: " + str(cou))
        if cou<3000000: # 2 million samples in the training set
            t_set.append(features)
        if cou>3000000: # 500k samples in test set
            v_set.append(features)

        cou+=1
        line = f.readline()

####### making and saving the csv files ###############

import csv

trainset_file="/content/gdrive/My Drive/Colab Notebooks/MLN/training.csv"
valset_file="/content/gdrive/My Drive/Colab Notebooks/MLN/validation.csv"

train_data=[]
test_data=[]

columns = ["text_ tokens", "hashtags", "tweet_id", "present_media", "present_links", "present_domains",\
                "tweet_type","language", "tweet_timestamp", "engaged_with_user_id", "engaged_with_user_follower_count",\
               "engaged_with_user_following_count", "engaged_with_user_is_verified", "engaged_with_user_account_creation",\
               "engaging_user_id", "engaging_user_follower_count", "engaging_user_following_count", "engaging_user_is_verified",\
               "engaging_user_account_creation", "engagee_follows_engager", "reply_timestamp", "retweet_timestamp", "retweet_with_comment_timestamp", "like_timestamp"]

for features in t_set:
    train_data.append(features)

for features in v_set:
    test_data.append(features)

with open(trainset_file,"w") as train_csv:
    csvwriter=csv.writer(train_csv)
    csvwriter.writerow(columns)
    csvwriter.writerows(train_data)

with open(valset_file,"w") as val_csv:
    csvwriter=csv.writer(val_csv)
    csvwriter.writerow(columns)
    csvwriter.writerows(test_data)