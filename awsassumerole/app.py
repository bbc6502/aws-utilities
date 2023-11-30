from argparse import ArgumentParser

import boto3


def main():
    parser = ArgumentParser(description='AWS assume role')
    parser.add_argument('--profile', help='AWS profile', required=True)
    parser.add_argument('--region', help='AWS region', default='ap-southeast-2')
    parser.add_argument('--role', help='AWS role to assume', required=True)
    parser.add_argument('--name', help='AWS role session name', default='assumed')
    args = parser.parse_args()
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    iam_client = session.client('iam')
    response = iam_client.get_role(RoleName=args.role)
    role_arn = response['Role']['Arn']
    sts_client = session.client('sts')
    response = sts_client.assume_role(RoleArn=role_arn, RoleSessionName=args.name)
    access_key_id = response['Credentials']['AccessKeyId']
    secret_access_key = response['Credentials']['SecretAccessKey']
    session_token = response['Credentials']['SessionToken']
    print(f'export AWS_ACCESS_KEY_ID={access_key_id}')
    print(f'export AWS_SECRET_ACCESS_KEY={secret_access_key}')
    print(f'export AWS_SESSION_TOKEN={session_token}')


if __name__ == '__main__':
    main()
