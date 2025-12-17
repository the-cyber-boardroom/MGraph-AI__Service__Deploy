from unittest                                                                       import TestCase
from osbot_utils.testing.Temp_Env_Vars                                              import Temp_Env_Vars
from osbot_utils.testing.__                                                         import __
from osbot_utils.testing.__helpers                                                  import obj
from osbot_utils.utils.Env                                                          import get_env
from osbot_utils.utils.Misc                                                         import random_text
from mgraph_ai_service_deploy.config                                                import ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_NAME, ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_VALUE, ENV_VAR__URL__TARGET_SERVER__GITHUB_SERVICE
from mgraph_ai_service_deploy.schemas.auth.Schema__Auth__Config__External_Service   import Schema__Auth__Config__External_Service
from mgraph_ai_service_deploy.services.Auth__External_Services                      import Auth__External_Services


class test_Auth__External_Services(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.auth_external_services = Auth__External_Services()

    def test__init__(self):
        with self.auth_external_services as _:
            assert type(_) is Auth__External_Services

    def test_config__graph_service(self):
        with self.auth_external_services.config__graph_service() as _:
            assert type(_) is Schema__Auth__Config__External_Service
            assert _.obj() == __(target_server = None,
                                 key_name      = None,
                                 key_value     = None,
                                 enabled       = False)

    def test_config__graph_service__with_env_vars(self):
        key_name      = random_text("an-key"  ).lower()
        key_value     = random_text("an-value").lower()
        target_server = "https://an-server/"
        env_vars = { ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_NAME   : key_name       ,
                     ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_VALUE  : key_value     ,
                     ENV_VAR__URL__TARGET_SERVER__GITHUB_SERVICE              : target_server }
        assert obj(env_vars)  == __(AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_NAME  = key_name     ,
                                    AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_VALUE = key_value    ,
                                    URL__TARGET_SERVER__GITHUB_SERVICE             = target_server)
        with Temp_Env_Vars(env_vars=env_vars):
            assert get_env(ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_NAME ) == key_name
            assert get_env(ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_VALUE) == key_value
            assert get_env(ENV_VAR__URL__TARGET_SERVER__GITHUB_SERVICE            ) == target_server

            with Auth__External_Services().config__graph_service() as _:
                assert _.obj() == __(target_server = target_server,
                                     key_name       = key_name    ,
                                     key_value      = key_value   ,
                                     enabled        = True        )
