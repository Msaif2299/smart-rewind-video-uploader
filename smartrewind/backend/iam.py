import json
from botocore.exceptions import ClientError

class IAM:
    def __init__(self, name, resource, sns_topic) -> None:
        self.name = name
        self.resource = resource
        self.topic = sns_topic
        self.role = None

    def create(self):
        try:
            self.role = self.resource.create_role(
                RoleName=self.name,
                AssumeRolePolicyDocument=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"Service": "rekognition.amazonaws.com"},
                                "Action": "sts:AssumeRole",
                            }
                        ],
                    }
                ),
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                try:
                    self.role = self.resource.Role(self.name)
                    self.role.load()
                except ClientError:
                    raise Exception(f"Couldn't load role {self.name}")
                print(f"Role {self.name} already exists, creating policy instead")
            else:
                raise Exception(json.dumps(e.response))
        try:
            policy = self.resource.create_policy(
                PolicyName=self.name,
                PolicyDocument=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Action": "SNS:Publish",
                                "Resource": self.topic.arn,
                            }
                        ],
                    }
                ),
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                try:
                    policies = list(self.resource.policies.filter(Scope='Local'))
                except ClientError as e:
                    raise Exception(f"Error while fetching policy {self.name}: {e}")
                is_policy_found = False
                for p in policies:
                    if p.meta.data['PolicyName'] == self.name:
                        policy, is_policy_found = p, True
                if not is_policy_found:
                    raise Exception(f"Policy {self.name} not found")
                print(f"Policy {self.name} already exists")
        self.role.attach_policy(PolicyArn=policy.arn)
        return self.role
    
    def get_role(self):
        if self.role is None:
            self.role = self.create()
        return self.role