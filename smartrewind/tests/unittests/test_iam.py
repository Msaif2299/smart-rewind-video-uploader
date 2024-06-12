from smartrewind.iam import IAM
from smartrewind.sns import SNS
import pytest
from ..mocks.sns import MockSNSResource
from ..mocks.iam import MockIAMResource, MockIAMResourceErrorCases

def test_iam_create():
    IAM("test", MockIAMResource(MockIAMResourceErrorCases()), SNS("test", MockSNSResource()).get_topic()).create()

def test_iam_create_role_client_error():
    with pytest.raises(Exception):
        IAM("test", MockIAMResource(MockIAMResourceErrorCases(raise_create_role_error=True)), SNS("test", MockSNSResource()).get_topic()).create()

def test_iam_create_role_client_error_entity_already_exists():
    IAM("test", MockIAMResource(MockIAMResourceErrorCases(raise_create_role_error_entity_already_exists=True)), SNS("test", MockSNSResource()).get_topic()).create()

def test_iam_create_policy_client_error():
    with pytest.raises(Exception):
        IAM("test", MockIAMResource(MockIAMResourceErrorCases(raise_create_policy_error=True)), SNS("test", MockSNSResource()).get_topic()).create()

def test_iam_create_policy_client_error_entity_already_exists():
    IAM("test", MockIAMResource(MockIAMResourceErrorCases(raise_create_policy_error_entity_already_exists=True)), SNS("test", MockSNSResource()).get_topic()).create()

def test_iam_policy_not_found():
    with pytest.raises(Exception):
        IAM("test", IAM("test", MockIAMResource(MockIAMResourceErrorCases(raise_policy_not_found_error=True)), SNS("test", MockSNSResource()).get_topic()).create())

def test_iam_get_role():
    IAM("test", MockIAMResource(MockIAMResourceErrorCases()), SNS("test", MockSNSResource()).get_topic()).get_role()