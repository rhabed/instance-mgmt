import json
import boto3
import logging

logging.basicConfig(level=logging.INFO)

def release_hosts():
    # TO DO
    pass


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
    myresponse={"Instances":[]}
    if 'Instances' in response:
        for instance in response['Instances']:
            if instance['State']['Name'] == 'stopped':
                logging.info(instance['InstanceId'])
                r = ec2_client.terminate_instances(InstanceIds=[instance['InstanceId']])
                logging.info(r)
                myresponse["Instances"].append(instance['InstanceId'])
        myresponse["status"]="instances terminated"
    else:
        logging.info("No instances to terminate")
        myresponse["status"]="No instances to terminate"
    return myresponse


def lambda_handler(event, context):
    logging.info("It's time to terminate the instance")
    response=terminate_instances()
    return response
