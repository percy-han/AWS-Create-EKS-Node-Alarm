import base64
import gzip
import boto3
import json
import io

region = 'us-west-2' #修改为您的region name
filter_name = 'New-Node-Join-EKS-Cluster' #修改为cloudwatch log 中的subscription filter name 
# 创建 CloudWatch 客户端
cloudwatch = boto3.client('cloudwatch', region_name=region)

def decode_and_decompress(encoded_data):
    try:
        # 解码 Base64 编码的内容
        decoded_data = base64.b64decode(encoded_data)

        # 使用 Gzip 解压缩
        with gzip.GzipFile(fileobj=io.BytesIO(decoded_data)) as gz_file:
            decompressed_data = gz_file.read()

        # 将字节数据解码为字符串
        decompressed_data = decompressed_data.decode('utf-8')
        json_data = json.loads(decompressed_data)

        return json_data
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error decoding or decompressing data: {e}")
        return None

def create_alarm(instance_id,region):
    try:
        alarm_description = 'This alarm is created by script to check instance StatusCheckFailed_System and trigger action'
        alarm_name = 'Alarm_EC2_StatusCheckFailed_System_' + instance_id
        # 定义 alarm 参数
        alarm_params = {
            'AlarmName': alarm_name,
            'AlarmDescription': alarm_description,
            'ActionsEnabled': True,
            'AlarmActions': [
                'arn:aws:automate:'+ region +':ec2:recover',  
            ],
            'MetricName': 'StatusCheckFailed_System',
            'Namespace': 'AWS/EC2',
            'Statistic': 'Maximum',
            'Dimensions': [
                {
                    'Name': 'InstanceId',
                    'Value': instance_id  
                },
            ],
            'Period': 60,  # 1 分钟
            'EvaluationPeriods': 1,
            'Threshold': 1,
            'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
            'Tags': [
                {
                    'Key': 'name',
                    'Value': 'auto-recovery-by-script'
                }
            ]
        }

        # 创建 alarm
        response = cloudwatch.put_metric_alarm(**alarm_params)
        print(response)
    except Exception as e:
        print(f"Error creating alarm for instance {instance_id}: {e}")

def lambda_handler(event, context):
    try:
        # 遍历 CloudWatch 日志事件
        event_json = decode_and_decompress(event['awslogs']['data'])
        if event_json:
            print(event_json)
            if event_json['subscriptionFilters'][0] == filter_name:
                print('Join Cluster')
                data_message = json.loads(event_json['logEvents'][0]['message'])
                response_code = data_message['responseStatus']['code']
                print(f'response code: {response_code}')
                instance_id = data_message['user']['extra']['sessionName'][0]
                print(f'New_Instance_Id: {instance_id}')
                if response_code == 200:
                    create_alarm(instance_id,region)
                else:
                    print('Instance Join EKS Cluster Failed!')
        else:
            print("Error decoding or decompressing data")
    except Exception as e:
        print(f"Error processing event: {e}")
