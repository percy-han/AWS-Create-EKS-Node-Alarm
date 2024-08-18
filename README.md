# AWS-Create-EKS-Node-Alarm
Create KES New Node instance alram by script
Limition:
Two subscription filter

# To create a Lambda
## Create IAM Policy <Lambda-EKS-Node-Alarm-Policy>
```
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
```

## Create IAM Role <Lambda-EKS-Node-Alarm-Role>

## Create Lambda Function
```
aws lambda create-function \
    --function-name Create-EKS-New-Node-Alarm \
    --zip-file fileb:///Users/havpan/Downloads/Create-EKS-Node-Alarm.zip \
    --role arn:aws:iam::887221633712:role/Lambda-EKS-Node-Alarm-Role \
    --handler lambda_function.lambda_handler \
    --runtime python3.10 \
    --region us-west-2
```

## Grant CloudWatch Logs the permission to execute your function. Use the following command, replacing the placeholder account with your own account and the placeholder log group with the log group to process:
```
aws lambda add-permission \
    --function-name "Create-EKS-New-Node-Alarm" \
    --statement-id "Create-EKS-New-Node-Alarm" \
    --principal "logs.amazonaws.com" \
    --action "lambda:InvokeFunction" \
    --source-arn "arn:aws:logs:us-west-2:887221633712:log-group:/aws/eks/eks-workshop/cluster:*" \
    --source-account "887221633712" \
    --region us-west-2
```


# Create a subscription filter using the following command, replacing the placeholder account with your own account and the placeholder log group with the log group to process
```aws logs put-subscription-filter \
    --log-group-name "/aws/eks/eks-workshop/cluster" \
    --filter-name New-Node-Join-EKS-Cluster \
    --filter-pattern "{ ($.apiVersion = \"audit.k8s.io/v1\") && ($.verb = \"patch\") &&($.objectRef.resource = \"nodes\") &&($.objectRef.subresource = \"status\") && ($.requestObject.status.conditions[3].type =  \"Ready\") &&  ($.requestObject.status.conditions[3].status =  \"True\")}" \
    --destination-arn arn:aws:lambda:us-west-2:887221633712:function:Create-EKS-New-Node-Alarm \
    --region us-west-2
```
