import json
import boto3
import logging

logging.basicConfig(level=logging.INFO)

def terminate_instances():
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'stopped',
            ]
        },
    ])
    for instance in response['Instances']:
        if instance['State']['Name'] == 'stopped':
            logging.info(instance['InstanceId'])
            r = ec2_client.terminate_instances(InstanceIds=[instance['InstanceId']])
            logging.info(r)


def lambda_handler(event, context):
    logging.info("It's time to terminate the instance")
    terminate_instances()


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
