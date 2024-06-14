from typing import List
from botocore.exceptions import ClientError
from dataclasses import dataclass

class MockRole:
    def __init__(self) -> None:
        self.arn = "test"
    def attach_policy(self, **kwargs):
        pass
    def load(self):
        pass

class MockPolicyData:
    def __init__(self, name) -> None:
        self.data = {"PolicyName": name}

class MockPolicy:
    def __init__(self, name) -> None:
        self.meta = MockPolicyData(name)
        self.arn = "DummyArn"

class MockPolicies:
    def __init__(self, name) -> None:
        self.list = [MockPolicy(name) for _ in range(5)]
    def filter(self, Scope) -> List[MockPolicy]:
        return self.list
    
@dataclass
class MockIAMResourceErrorCases:
    raise_create_role_error: bool = False
    raise_create_role_error_entity_already_exists: bool = False
    raise_create_policy_error: bool = False
    raise_create_policy_error_entity_already_exists: bool = False
    raise_policy_not_found_error: bool = False
    raise_mock_policy_error: bool = False

class MockIAMResource:
    def __init__(self, raise_error: MockIAMResourceErrorCases = MockIAMResourceErrorCases()) -> None:
        self.raise_error = raise_error
    def create_role(self, **kwargs) -> MockRole:
        if self.raise_error.raise_create_role_error:
            raise ClientError({
                "Error": {
                    "Code": "EntityNotFound",
                    "Message": "Create IAM Role Failed"
                }
            }, "Create IAM Role")
        if self.raise_error.raise_create_role_error_entity_already_exists:
            raise ClientError({
                "Error": {
                    "Code": "EntityAlreadyExists",
                    "Message": "Create IAM Role Failed"
                }
            }, "Create IAM Role")
        return MockRole()
    def Role(self, *args, **kwargs) -> MockRole:
        return MockRole()
    def create_policy(self, PolicyName, **kwargs):
        self.policies = MockPolicies(PolicyName)
        if self.raise_error.raise_policy_not_found_error:
            self.policies = MockPolicies(PolicyName + "break")
        if self.raise_error.raise_create_policy_error:
            raise ClientError({
                "Error": {
                    "Code": "EntityNotFound",
                    "Message": "Create IAM Policy Failed"
                }
            }, "Create IAM Role")
        if self.raise_error.raise_create_policy_error_entity_already_exists:
            raise ClientError({
                "Error": {
                    "Code": "EntityAlreadyExists",
                    "Message": "Create IAM Policy Failed"
                }
            }, "Create IAM Role")
        return MockPolicy(PolicyName)
