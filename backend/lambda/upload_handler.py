import boto3
import json
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = 'smartexpense-receipts-chandhana'

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': ''
        }

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
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': json.dumps({'file_key': file_name})
    }