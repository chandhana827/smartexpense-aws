import boto3
import json
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = 'smartexpense-receipts-chandhana'

def lambda_handler(event, context):
    body = json.loads(event['body'])
    image_data = body['image']
    file_name = f"receipts/{uuid.uuid4()}.jpg"
    
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=image_data,
        ContentType='image/jpeg'
    )
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'file_key': file_name})
    }