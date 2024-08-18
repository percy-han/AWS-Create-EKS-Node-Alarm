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
##Create IAM Role <Lambda-EKS-Node-Alarm-Role>
