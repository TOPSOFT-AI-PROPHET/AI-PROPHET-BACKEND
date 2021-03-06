import os
import tempfile
from io import BytesIO

import joblib
from qcloud_cos import CosConfig, CosS3Client

secret_id = os.getenv("COS_SECRET_ID")
secret_key = os.getenv("COS_SECRET_KEY")
region = os.getenv("COS_REGION")
bucket = os.getenv("COS_BUCKET")
token = None
scheme = "https"
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)

# Write single model to bucket
def write_model(key, model):
    with tempfile.TemporaryFile() as fp:
        joblib.dump(model, fp)
        fp.seek(0)
        response = client.put_object(Bucket=bucket, Body=fp, Key=key, StorageClass="STANDARD", EnableMD5=False)
        return response


# Read a single model in bucket
def read_model(key):
    response = client.get_object(Bucket=bucket, Key=key)
    bytes = BytesIO(response["Body"].get_raw_stream().read())
    model = joblib.load(bytes)
    return model


def put_object(key, body):
    response = client.put_object(Bucket=bucket, Body=body, Key=key, StorageClass="STANDARD", EnableMD5=False)
    return response


# Delete object in bucket
def delete_object(key):
    response = client.delete_object(Bucket=bucket, Key=key)
    return response
