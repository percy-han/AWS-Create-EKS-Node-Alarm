# AWS-Create-EKS-Node-Alarm
AWS instance级别的告警可以出发多种action，比如：auto-recovery,auto-scaling,执行lambda，发送通知等。然而该告警的配置是实例级别的，即只能为每一台实例配置告警，而无法配置一个统计模版。更重要的是，在生产环境中并非所有的workload都需要如此配置。这里以EKS集群为例，说明下当EKS集群扩容之后如何对新增节点配置instance级别的告警

## Limition:
Each log group can have up to two subscription filters associated with it!


## Create IAM Policy 
Policy Nmae: Lambda-EKS-Node-Alarm-Policy
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

## Create IAM Role 
Role Name: Lambda-EKS-Node-Alarm-Role
![image](https://github.com/user-attachments/assets/64b99973-955c-4e36-aaa6-bfd3e3501f7c)

![image](https://github.com/user-attachments/assets/41c00fdd-198e-4c1e-a3ad-08cb4dba5775)


## Create Lambda Function
```
aws lambda create-function \
    --function-name Create-EKS-New-Node-Alarm \
    --zip-file fileb:///Users/havpan/Downloads/Create-EKS-Node-Alarm.zip \
    --role arn:aws:iam::887221633712:role/Lambda-EKS-Node-Alarm-Role \
    --handler lambda_function.lambda_handler \
    --runtime python3.10 \
    --region <your-region>
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


## Create a subscription filter using the following command, replacing the placeholder account with your own account and the placeholder log group with the log group to process
```
aws logs put-subscription-filter \
    --log-group-name "/aws/eks/eks-workshop/cluster" \
    --filter-name New-Node-Join-EKS-Cluster \
    --filter-pattern "{ ($.apiVersion = \"audit.k8s.io/v1\") && ($.verb = \"patch\") &&($.objectRef.resource = \"nodes\") &&($.objectRef.subresource = \"status\") && ($.requestObject.status.conditions[3].type =  \"Ready\") &&  ($.requestObject.status.conditions[3].status =  \"True\")}" \
    --destination-arn arn:aws:lambda:us-west-2:887221633712:function:Create-EKS-New-Node-Alarm \
    --region us-west-2
```
