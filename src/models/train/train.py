import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
import lightgbm as lgb
from google.cloud import storage
import os
import joblib

# Set environment variables for your project and buckets
PROJECT_ID = 'cdp-demo-395508'
DATA_BUCKET_NAME = f"{PROJECT_ID}-ai-landingzone-datasets"
MODEL_BUCKET_NAME = f"{PROJECT_ID}-ai-landingzone-models"
DATA_BLOB_NAME = 'iris.csv'
MODEL_FILE_NAME = "model.pkl"

# Initialize GCS client
storage_client = storage.Client(project=PROJECT_ID)

# Download the dataset from the data bucket
data_bucket = storage_client.get_bucket(DATA_BUCKET_NAME)
data_blob = data_bucket.blob(DATA_BLOB_NAME)
local_iris_file = 'iris.csv'
data_blob.download_to_filename(local_iris_file)

# Read the dataset from the local file
attributes = ["sepal_length", "sepal_width", "petal_length", "petal_width", "class"]
dataset = pd.read_csv(local_iris_file, names=attributes)
dataset.columns = attributes

# Split dataset into train and test sets
train, test = train_test_split(dataset, test_size=0.4, stratify=dataset['class'], random_state=42)
X_train = train[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
y_train = train['class']
X_test = test[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
y_test = test['class']

# Train the LightGBM model
model = lgb.LGBMClassifier()
model.fit(X_train, y_train)
prediction = model.predict(X_test)

# Save the model to a local file
joblib.dump(model, MODEL_FILE_NAME)

# Upload the model artifact to the model bucket
model_bucket = storage_client.get_bucket(MODEL_BUCKET_NAME)
model_blob = model_bucket.blob('model/' + MODEL_FILE_NAME)
model_blob.upload_from_filename(MODEL_FILE_NAME)

print("Successfully Uploaded Model to Model Bucket!")

# Print accuracy
print('The accuracy of the LightGBM model is', "{:.3f}".format(metrics.accuracy_score(prediction, y_test)))
