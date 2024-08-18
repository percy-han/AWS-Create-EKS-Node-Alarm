# AWS-Create-EKS-Node-Alarm
Create KES New Node instance alram by script
Limition:
Two subscription filter

# To create a Lambda
## Create IAM Policy <Lambda-EKS-Node-Alarm-Policy>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "cloudwatch:PutMetricAlarm",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],
            "Resource": "*"
        }
    ]
}

## Create IAM Role <Lambda-EKS-Node-Alarm-Role>

## Create Lambda Function
aws lambda create-function \
    --function-name Create-EKS-New-Node-Alarm \
    --zip-file fileb:///Users/havpan/Downloads/Create-EKS-Node-Alarm.zip \
    --role arn:aws:iam::887221633712:role/Lambda-EKS-Node-Alarm-Role \
    --handler lambda_function.lambda_handler \
    --runtime python3.10 \
    --region us-west-2
