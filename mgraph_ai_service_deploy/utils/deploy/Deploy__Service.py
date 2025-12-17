from osbot_fast_api_serverless.deploy.Deploy__Serverless__Fast_API import Deploy__Serverless__Fast_API
from osbot_utils.utils.Env import get_env

from mgraph_ai_service_deploy.config import SERVICE_NAME, LAMBDA_DEPENDENCIES__DEPLOY__SERVICE, ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_NAME, \
    ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_VALUE, ENV_VAR__URL__TARGET_SERVER__GITHUB_SERVICE
from mgraph_ai_service_deploy.fast_api.lambda_handler              import run


class Deploy__Service(Deploy__Serverless__Fast_API):

    def deploy_lambda(self):
        with super().deploy_lambda() as _:
            # Add any service-specific environment variables here
            env_vars = [ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_NAME ,
                        ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_VALUE,
                        ENV_VAR__URL__TARGET_SERVER__GITHUB_SERVICE            ]
            for env_var in env_vars:
                _.set_env_variable(env_var, get_env(env_var))
            return _

    def handler(self):
        return run

    def lambda_dependencies(self):
        return LAMBDA_DEPENDENCIES__DEPLOY__SERVICE

    def lambda_name(self):
        return SERVICE_NAME
