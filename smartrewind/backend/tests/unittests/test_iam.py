import pytest

from smartrewind.backend.iam import IAM
from smartrewind.backend.sns import SNS
from smartrewind.backend.tests.mocks.sns import MockSNSResource
from smartrewind.backend.tests.mocks.iam import MockIAMResource, MockIAMResourceErrorCases
from smartrewind.logger import Logger

@pytest.fixture(autouse=True)
def logger():
    logger = Logger("", True)
    yield logger

def test_iam_create(logger: Logger):
    IAM(
        "test", 
        MockIAMResource(MockIAMResourceErrorCases()), 
        SNS("test", MockSNSResource(), logger).get_topic(), 
        logger
    ).create()

def test_iam_create_role_client_error(logger: Logger):
    with pytest.raises(Exception):
        IAM(
            "test", 
            MockIAMResource(MockIAMResourceErrorCases(raise_create_role_error=True)), 
            SNS("test", MockSNSResource(), logger).get_topic(), 
            logger
        ).create()

def test_iam_create_role_client_error_entity_already_exists(logger: Logger):
    IAM(
        "test", 
        MockIAMResource(MockIAMResourceErrorCases(raise_create_role_error_entity_already_exists=True)), 
        SNS("test", MockSNSResource(), logger).get_topic(), 
        logger
    ).create()

def test_iam_create_policy_client_error(logger: Logger):
    with pytest.raises(Exception):
        IAM(
            "test", 
            MockIAMResource(MockIAMResourceErrorCases(raise_create_policy_error=True)), 
            SNS("test", MockSNSResource(), logger).get_topic(), 
            logger
        ).create()

def test_iam_create_policy_client_error_entity_already_exists(logger: Logger):
    IAM(
        "test", 
        MockIAMResource(MockIAMResourceErrorCases(raise_create_policy_error_entity_already_exists=True)), 
        SNS("test", MockSNSResource(), logger).get_topic(), 
        logger
    ).create()

def test_iam_policy_not_found(logger: Logger):
    with pytest.raises(Exception):
        IAM(
            "test", 
            IAM("test", MockIAMResource(MockIAMResourceErrorCases(raise_policy_not_found_error=True)), 
            SNS("test", MockSNSResource(), logger).get_topic(), 
            logger
        ).create())

def test_iam_get_role(logger: Logger):
    IAM(
        "test", 
        MockIAMResource(MockIAMResourceErrorCases()), 
        SNS("test", MockSNSResource(), logger).get_topic(), 
        logger
    ).get_role()