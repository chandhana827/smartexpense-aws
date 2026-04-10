# smartexpense-aws

# SmartExpense — Receipt Analyzer

![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=FF9900)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

---

## What is this?

I built this project to solve a simple problem — I never knew where my money was going every month. I had receipts from grocery stores, restaurants, and random shopping trips but tracking them manually was a pain.

So I built SmartExpense. You take a photo of any receipt, upload it, and the app tells you what category the expense belongs to and pulls out the important details automatically. No typing, no manual entry.

---

## Live Demo
👉 [https://chandhana827.github.io/smartexpense-aws/](https://chandhana827.github.io/smartexpense-aws/)

---

## How it actually works

When you upload a receipt image, here is what happens behind the scenes:

**Step 1 — Image gets stored**
The image goes straight to an AWS S3 bucket. Nothing fancy, just secure cloud storage.

**Step 2 — AI reads the receipt**
AWS Textract scans the image and pulls out all the text. This is the same OCR technology Amazon uses internally. It handles blurry images, different fonts, and even handwritten text surprisingly well.

**Step 3 — AI finds the important stuff**
The extracted text goes to AWS Comprehend which picks out key phrases — things like store names, item names, and amounts.

**Step 4 — It figures out the category**
Based on the words in the receipt, the app puts it into one of these buckets:
- Food & Dining
- Transport
- Shopping
- Healthcare
- General

**Step 5 — Everything gets saved**
The expense details go into a DynamoDB table with a unique ID and timestamp so nothing is lost.

The whole thing runs on AWS Lambda — no server to manage, no monthly hosting cost.

---

## Why I used these AWS services

I wanted to keep this entirely on AWS Free Tier and learn how these services work together. Here is what each one does:

| Service | Why I used it |
|---|---|
| S3 | Cheap, reliable image storage |
| Textract | Best OCR I could find for receipts |
| Comprehend | Good at pulling meaning from messy text |
| Lambda | No server needed, scales automatically |
| DynamoDB | Simple NoSQL storage, free tier is generous |
| Lambda Function URL | Quick API without setting up a full API Gateway |

---

## Project structure
smartexpense-aws/
├── frontend/
│   └── index.html
├── backend/
│   └── lambda/
│       ├── upload_handler.py
│       └── analyze_handler.py
├── index.html
├── trust-policy.json
├── .gitignore
└── README.md

---

## Running this yourself

You need an AWS account and AWS CLI set up on your machine.

```bash
git clone https://github.com/chandhana827/smartexpense-aws.git
cd smartexpense-aws
aws configure
```

Create the S3 bucket:
```bash
aws s3api create-bucket --bucket YOUR-BUCKET-NAME --region us-east-1
```

Create the DynamoDB table:
```bash
aws dynamodb create-table \
  --table-name Expenses \
  --attribute-definitions AttributeName=expense_id,AttributeType=S \
  --key-schema AttributeName=expense_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

Deploy the Lambda functions:
```bash
cd backend/lambda
zip upload_handler.zip upload_handler.py
zip analyze_handler.zip analyze_handler.py

aws lambda create-function --function-name smartexpense-upload \
  --runtime python3.12 \
  --role YOUR-IAM-ROLE-ARN \
  --handler upload_handler.lambda_handler \
  --zip-file fileb://upload_handler.zip

aws lambda create-function --function-name smartexpense-analyze \
  --runtime python3.12 \
  --role YOUR-IAM-ROLE-ARN \
  --handler analyze_handler.lambda_handler \
  --zip-file fileb://analyze_handler.zip
```

Then update the Lambda URLs in `index.html` and you are good to go.

---

## What I learned building this

This was my first time connecting multiple AWS services together in one project. A few things that took me longer than expected:

- IAM permissions are tricky. Getting the Lambda role to have exactly the right access took some trial and error.
- CORS is always annoying. Even with Lambda Function URLs, getting the headers right needed a few attempts.
- AWS CLI on Windows PowerShell behaves differently from Linux — JSON escaping is a headache.

Overall it was a good learning experience for understanding how real cloud applications are built.

---

## What I want to add next

- Monthly spending summary with a chart
- Support for PDF receipts
- Login system so multiple users can track their own expenses
- Smarter categorization using Amazon Bedrock

---

## Built by

Chandhana — [@chandhana827](https://github.com/chandhana827)
