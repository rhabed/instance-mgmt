import json
import boto3
import logging

logging.basicConfig(level=logging.INFO)

def release_hosts():
    # TO DO
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_hosts(Filters=[
        {
            'Name': 'state',
            'Values': [
                'available'
            ]
        }
    ])
    myresponse={"Hosts":[]}
    if 'Hosts' in response:
        for host in response['Hosts']:
            if host['State'] == 'available' and host['Instances'] == []:
                logging.info(host['HostId'])
                r = ec2_client.release_hosts(HostIds=[host['HostId']])
                logging.info(r)
                myresponse["Hosts"].append(host['HostId'])
            else:
                logging.error(f"{host['HostId']} cannot be released - instances running in host:  {host['Instances']}")
        myresponse["status"]="hosts released"
    else:
        logging.info("No hosts to release")
        myresponse["status"]="No hosts to release"
    return myresponse


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
    terminate_instances()
    release_hosts()