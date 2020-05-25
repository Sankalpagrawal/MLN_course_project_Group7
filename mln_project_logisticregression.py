# -*- coding: utf-8 -*-
"""MLN_project_logisticregression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hsrcLwkpQyI7aSUxz_arY7XTCGAbOvMc
"""

from google.colab import drive

drive.mount('/content/gdrive/',force_remount=True)

import csv

def make_train_sets(output_var,number_of_samples):
    positives = 0
    negatives = 0
    
    train_set = []
    counter=0
    with open("/content/gdrive/My Drive/training.csv","r") as csvfile:
        csvreader=csv.reader(csvfile)
        columns=csvreader.__next__()
        for row in csvreader:
            counter+=1

            if row[output_var]=='':
                if output_var==20 and negatives==225000:
                    continue
                elif (output_var==21 or output_var==23) and negatives==int(number_of_samples/2):
                    continue
                elif output_var==22 and negatives==279000:
                    continue
                negatives+=1
                train_set.append(row)
            else:
                if positives==int(number_of_samples/2):
                    continue
                positives+=1
                train_set.append(row)
            
            if (output_var==23 or output_var==21) and negatives==int(number_of_samples/2) and positives==int(number_of_samples/2):
                break
            if output_var==20 and positives==75000:
                break
            if output_var==22 and positives==21000:
                break
    return train_set

def make_val_sets(output_var,number_of_samples):
    positives = 0
    negatives = 0
    
    val_set = []
    counter=0
    with open("/content/gdrive/My Drive/validation.csv","r") as csvfile:
        csvreader=csv.reader(csvfile)
        columns=csvreader.__next__()
        for row in csvreader:
            counter+=1

            if row[output_var]=='':
                if output_var==20 and negatives==number_of_samples-18000:
                    continue
                elif (output_var==21 or output_var==23) and negatives==int(number_of_samples/2):
                    continue
                elif output_var==22 and negatives==number_of_samples-5200:
                    continue
                negatives+=1
                val_set.append(row)
            else:
                positives+=1
                val_set.append(row)
            
            if (output_var==23 or output_var==21) and negatives==int(number_of_samples/2) and positives==int(number_of_samples/2):
                break
            if output_var==20 and positives==18000:
                break
            if output_var==22 and positives==5200:
                break
    return val_set

valset_file="/content/gdrive/My Drive/validation.csv"
trainset_file="/content/gdrive/My Drive/training.csv"

train_set1 = make_train_sets(20,300000)
train_set2 = make_train_sets(21,300000)
train_set3 = make_train_sets(22,300000)
train_set4 = make_train_sets(23,300000)

val_set1 = make_val_sets(20,90000)
val_set2 = make_val_sets(21,90000)
val_set3 = make_val_sets(22,90000)
val_set4 = make_val_sets(23,90000)

# Tweet text features
import numpy as np
from sklearn.decomposition import PCA

def encode_text_encodings(values_set):
    tweet_texts = []
    for row in values_set:
        tweet_texts.append( list(map(int,row[0].split('\t'))) )

    len_tweet_texts = []
    for i in tweet_texts:
        len_tweet_texts.append(len(i))

    text_enc = np.zeros((len(values_set),max(len_tweet_texts)))

    for i in range(len(values_set)):
        text_enc[i,:len(tweet_texts[i])] = tweet_texts[i]

    pca = PCA(n_components=16)
    pca.fit(text_enc)
    transformed_vector = pca.transform(text_enc)
    return transformed_vector

tweet_data_train1 = encode_text_encodings(train_set1)
tweet_data_train2 = encode_text_encodings(train_set2)
tweet_data_train3 = encode_text_encodings(train_set3)
tweet_data_train4 = encode_text_encodings(train_set4)

tweet_data_val1 = encode_text_encodings(val_set1)
tweet_data_val2 = encode_text_encodings(val_set2)
tweet_data_val3 = encode_text_encodings(val_set3)
tweet_data_val4 = encode_text_encodings(val_set4)

# Rest features: numerical, categorical and ID features

def normalize_matrix(data):
    m,n = data.shape
    for i in range(n):
        x = data[:,i]
        norm = (x - x.min()) / (x.max() -x.min()) # Min max normalization
        data[:,i] = norm
    return data 

def normalize(data):
    minim = min(data)
    maxim = max(data)

    for val in range(len(data)):
        data[val] = (data[val] - minim) / (maxim-minim)

    return data

# For number of hashtags, media, links and domains (features #1, #3, #4, #5)
# For number of followers, followees ( features #10, #11, #15, #16)
def encode_numerical_data(values_set,parameter):

    if parameter==1 or parameter==3 or parameter==4 or parameter==5:
        data = []
        for row in values_set:
            if row[parameter]=='':
                data.append([0])
            else:
                data.append(row[parameter].split('\t'))
        
        len_data = []
        for i in data:
            if i==[0]:
                len_data.append(0)
            else:
                len_data.append(len(i))

        return normalize(len_data)

    else:
        data = []
        for row in values_set:
            data.append(int(row[parameter]))
        return normalize(data)

def encode_categorical_data(values_set,parameter):
    data = []
    for row in values_set:
        if parameter==12 or parameter==17 or parameter==19 or parameter==20 or parameter==21 or parameter==22 or parameter==23:
            if row[parameter]=='' or row[parameter]=='false':
                data.append(0)
            else:
                data.append(1)
        
        if parameter==6:
            if row[parameter]=='Quote':
                data.append(1)
            elif row[parameter]=='Retweet':
                data.append(2)
            elif row[parameter]=='TopLevel':
                data.append(3)
            else:
                data.append(4)

    return normalize(data)

# For features #2, #7 and #9 and #14
def encode_ID_data(values_set,parameter):
    data = []
    for row in values_set:
        s = row[parameter]
        data.append(abs(hash(s)) % (10 ** 8))

    return normalize(data)

# Making the final input vector (concatenation of tweet (size 16) and all other vectors (total 16))

def get_inputs_outputs(tweet_data,values_set):
    mat1 = normalize_matrix(tweet_data)
    mat2 = np.zeros((len(values_set),16))

    mat_labels = np.zeros((len(values_set),4))

    mat2[:,0] = encode_numerical_data(values_set,1)
    mat2[:,1] = encode_ID_data(values_set,2)
    mat2[:,2] = encode_numerical_data(values_set,3)
    mat2[:,3] = encode_numerical_data(values_set,4)
    mat2[:,4] = encode_numerical_data(values_set,5)
    mat2[:,5] = encode_categorical_data(values_set,6)
    mat2[:,6] = encode_ID_data(values_set,7)
    mat2[:,7] = encode_ID_data(values_set,9)
    mat2[:,8] = encode_numerical_data(values_set,10)
    mat2[:,9] = encode_numerical_data(values_set,11)
    mat2[:,10] = encode_categorical_data(values_set,12)
    mat2[:,11] = encode_ID_data(values_set,14)
    mat2[:,12] = encode_numerical_data(values_set,15)
    mat2[:,13] = encode_numerical_data(values_set,16)
    mat2[:,14] = encode_categorical_data(values_set,17)
    mat2[:,15] = encode_categorical_data(values_set,19)
    
    mat_labels[:,0] = encode_categorical_data(values_set,20)
    mat_labels[:,1] = encode_categorical_data(values_set,21)
    mat_labels[:,2] = encode_categorical_data(values_set,22)
    mat_labels[:,3] = encode_categorical_data(values_set,23)

    mat_inputs = np.concatenate((mat1,mat2),axis=1)

    return mat_inputs, mat_labels

inputs_train1, outputs_train1 = get_inputs_outputs(tweet_data_train1,train_set1)
inputs_val1, outputs_val1 = get_inputs_outputs(tweet_data_val1,val_set1)

inputs_train2, outputs_train2 = get_inputs_outputs(tweet_data_train2,train_set2)
inputs_val2, outputs_val2 = get_inputs_outputs(tweet_data_val2,val_set2)

inputs_train3, outputs_train3 = get_inputs_outputs(tweet_data_train3,train_set3)
inputs_val3, outputs_val3 = get_inputs_outputs(tweet_data_val3,val_set3)

inputs_train4, outputs_train4 = get_inputs_outputs(tweet_data_train4,train_set4)
inputs_val4, outputs_val4 = get_inputs_outputs(tweet_data_val4,val_set4)

####### Logistic Regression ########

from sklearn.linear_model import LogisticRegression

clf1 = LogisticRegression(penalty='l2', solver='saga')
model1 = clf1.fit(inputs_train1, outputs_train1[:,0])
print("Trained")
y1 = model1.predict(inputs_val1)

clf2 = LogisticRegression(penalty='l2', solver='saga')
model2 = clf2.fit(inputs_train2, outputs_train2[:,1])
print("Trained")
y2 = model2.predict(inputs_val2)

clf3 = LogisticRegression(penalty='l2', solver='saga')
model3 = clf3.fit(inputs_train3, outputs_train3[:,2])
print("Trained")
y3 = model3.predict(inputs_val3)

clf4 = LogisticRegression(penalty='l2', solver='saga')
model4 = clf4.fit(inputs_train4, outputs_train4[:,3])
print("Trained")
y4 = model4.predict(inputs_val4)

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

print("Accuracy of Prediction for Reply engagement: " + str(accuracy_score(outputs_val1[:,0],y1)))
print("Accuracy of Prediction for Retweet engagement: " + str(accuracy_score(outputs_val2[:,1],y2)))
print("Accuracy of Prediction for Retweet with comment engagement: " + str(accuracy_score(outputs_val3[:,2],y3)))
print("Accuracy of Prediction for Like engagement: " + str(accuracy_score(outputs_val4[:,3],y4)))

y1_train = model1.predict(inputs_train1)
y2_train = model2.predict(inputs_train2)
y3_train = model3.predict(inputs_train3)
y4_train = model4.predict(inputs_train4)

print("Training accuracy for Reply engagement: " + str(accuracy_score(outputs_train1[:,0],y1_train)))
print("Training accuracy for Retweet engagement: " + str(accuracy_score(outputs_train2[:,1],y2_train)))
print("Training accuracy for Retweet with comment engagement: " + str(accuracy_score(outputs_train3[:,2],y3_train)))
print("Training accuracy for Like engagement: " + str(accuracy_score(outputs_train4[:,3],y4_train)))

m1 = confusion_matrix(outputs_val1[:,0],y1)
m2 = confusion_matrix(outputs_val2[:,1],y2)
m3 = confusion_matrix(outputs_val3[:,2],y3)
m4 = confusion_matrix(outputs_val4[:,3],y4)

print("Confusion Matrix for Reply engagement: ")
print(m1)
print("Confusion Matrix for Retweet engagement: ")
print(m2)
print("Confusion Matrix for Retweet with comment engagement: ")
print(m3)
print("Confusion Matrix for Like engagement: ")
print(m4)

from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

r1 = roc_auc_score(outputs_val1[:,0],y1)
r2 = precision_score(outputs_val1[:,0],y1)
r3 = recall_score(outputs_val1[:,0],y1)

r4 = roc_auc_score(outputs_val2[:,0],y2)
r5 = precision_score(outputs_val2[:,0],y2)
r6 = recall_score(outputs_val2[:,0],y2)

r7 = roc_auc_score(outputs_val3[:,0],y3)
r8 = precision_score(outputs_val3[:,0],y3)
r9 = recall_score(outputs_val3[:,0],y3)

r10 = roc_auc_score(outputs_val4[:,0],y4)
r11 = precision_score(outputs_val4[:,0],y4)
r12 = recall_score(outputs_val4[:,0],y4)

print("ROC-AUC score for Reply engagement: ")
print(r1)
print("Precision for Reply engagement: ")
print(r2)
print("Recall for Reply engagement: ")
print(r3)

print("ROC-AUC score for Retweet engagement: ")
print(r4)
print("Precision for Retweet engagement: ")
print(r5)
print("Recall for Retweet engagement: ")
print(r6)

print("ROC-AUC score for Retweet,comment engagement: ")
print(r7)
print("Precision for Retweet,comment engagement: ")
print(r8)
print("Recall for Retweet,comment engagement: ")
print(r9)

print("ROC-AUC score for Reply engagement: ")
print(r10)
print("Precision for Reply engagement: ")
print(r11)
print("Recall for Reply engagement: ")
print(r12)