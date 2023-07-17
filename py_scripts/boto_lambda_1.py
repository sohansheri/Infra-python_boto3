# Script to run lamda fucntion of Amazon recognition

from http import client
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
metadata_table = os.environ["METADATA_TABLE"]

#initiating the client reko and dyanamodb in function

def lambda_handler(event, context):
    reko_client = boto3.client("rekognition")
    dynamodb_resource = boto3.resource("dynamodb")

    for record in event["Records"]:
        bucket_name = record["s3"]["bucket"]["name"]
        image_obj = record["s3"]["object"]["key"]

        amount_faces = 0
        male_faces = 0
        female_faces = 0
        beard_faces = 0
        eyeglass_faces = 0
        sunglas_faces = 0
        mustache = 0

        print(amount_faces)
        print(male_faces)
        print(female_faces)
        print(image_obj)
        print(bucket_name)

        response = reko_client.detect_faces(Image={'S3Object':{'Bucket':bucket_name,'Name':image_obj}},Attributes=['ALL'])
        faces = response["FaceDetails"]

        amount_faces = len(faces)
        print(amount_faces)

        for face in faces:
            if face["Gender"]["Value"] == "Male":
                male_faces += 1
            if face["Beard"]["Value"] == True:
                beard_faces += 1
            if face["Eyeglasses"]["Value"] == True:
                eyeglass_faces +=1
            if face["Sunglasses"]["Value"] == True:
                sunglas_faces +=1
            if face["Mustache"]["Value"] == True:
                mustache += 1
            elif face["Gender"]["Value"] == "Female":
                female_faces += 1

        print(male_faces)
        print(female_faces)

        table = dynamodb_resource.Table(metadata_table)

        metadata = {
            "filename": image_obj,
            "amount_of_faces": amount_faces,
            "male_faces": male_faces,
            "female_faces": female_faces,
            "Eyeglasses" : eyeglass_faces,
            "sunglases" : sunglas_faces,
            "beard": beard_faces,
            "mustache": mustache
        }

        table.put_item(Item=metadata)





