import boto3
import json
import uuid
from datetime import datetime

textract = boto3.client('textract', region_name='us-east-1')
comprehend = boto3.client('comprehend', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

BUCKET_NAME = 'smartexpense-receipts-chandhana'
TABLE_NAME = 'Expenses'

def lambda_handler(event, context):
    # Handle CORS preflight
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

    try:
        body = json.loads(event['body'])
        file_key = body['file_key']

        # Step 1: Extract text using Textract
        textract_response = textract.detect_document_text(
            Document={'S3Object': {'Bucket': BUCKET_NAME, 'Name': file_key}}
        )

        extracted_text = " ".join([
            block['Text']
            for block in textract_response['Blocks']
            if block['BlockType'] == 'LINE'
        ])

        # Step 2: Analyze using Comprehend
        key_phrases = comprehend.detect_key_phrases(
            Text=extracted_text[:4000],
            LanguageCode='en'
        )

        # Step 3: Categorize expense
        category = categorize_expense(extracted_text)

        # Step 4: Save to DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        expense_id = str(uuid.uuid4())
        table.put_item(Item={
            'expense_id': expense_id,
            'raw_text': extracted_text,
            'category': category,
            'timestamp': datetime.now().isoformat()
        })

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'expense_id': expense_id,
                'extracted_text': extracted_text,
                'category': category,
                'key_phrases': [p['Text'] for p in key_phrases['KeyPhrases'][:5]]
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }

def categorize_expense(text):
    text = text.lower()
    if any(word in text for word in ['restaurant', 'cafe', 'food', 'pizza', 'burger', 'swiggy', 'zomato']):
        return 'Food & Dining'
    elif any(word in text for word in ['uber', 'ola', 'fuel', 'petrol', 'taxi', 'rapido']):
        return 'Transport'
    elif any(word in text for word in ['amazon', 'flipkart', 'shopping', 'mall', 'myntra']):
        return 'Shopping'
    elif any(word in text for word in ['hospital', 'pharmacy', 'medical', 'doctor', 'apollo']):
        return 'Healthcare'
    else:
        return 'General'