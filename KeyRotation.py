import json
import boto3

def lambda_handler(event, context):
    username ='pavan' #Enter your IAM USER name 
    iam = boto3.client('iam')
    
    response = iam.list_access_keys(UserName=username)
    
    access_keys = response['AccessKeyMetadata']
    
    # Deleting all previous access keys
    for access_key in access_keys:
        access_key_id = access_key['AccessKeyId']
        print(f"Deleting Access Key: {access_key_id}")
        iam.delete_access_key(UserName=username, AccessKeyId=access_key_id)
   
    # Creating a new Access Key
    print("Creating a new Access Key")
    response = iam.create_access_key(UserName=username)
    new_access_key_id = response['AccessKey']['AccessKeyId']
    new_secret_access_key = response['AccessKey']['SecretAccessKey']
    
    print(f"New Access Key ID: {new_access_key_id}")
    print(f"New Secret Access Key: {new_secret_access_key}")
    
    sns_message = f"IAM user {username}'s access key has been rotated. New Access Key ID: {new_access_key_id} & New SecretKey ID: {new_secret_access_key}"
    
    sns_topic_arn = 'Replace with your sns topic arn'
    
    sns = boto3.client('sns')
    
    sns.publish(TopicArn=sns_topic_arn, Message=sns_message, Subject="IAM User Access Key Rotation")
    
    print("Successfully Rotated keys and sent email to the user")
    




