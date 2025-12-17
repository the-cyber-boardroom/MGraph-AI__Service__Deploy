from unittest                                    import TestCase

from osbot_utils.utils.Env import load_dotenv
from osbot_utils.utils.Files import path_combine

from tests import deploy_aws
from tests.deploy_aws.test_Deploy__Service__base import test_Deploy__Service__base

class test_Deploy__Service__to__dev(test_Deploy__Service__base, TestCase):
    stage = 'dev'

    # @classmethod
    # def setUpClass(cls):
    #     env_file = path_combine(deploy_aws.path, '.deploy.env')
    #     load_dotenv(dotenv_path=env_file, override=True)
    #     super().setUpClass()
    #
    # def test_3__install_again(self):
    #     self.test_3__create()
    #
    # def test_4__invoke__return_logs(self):
    #     self.test_3__create()
    #     from osbot_utils.utils.Dev import pprint
    #     payload = {}
    #     response = self.deploy_fast_api.lambda_function().invoke(payload)
    #     pprint(response)