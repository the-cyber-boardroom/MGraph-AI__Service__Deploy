from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.utils.Env                                                                  import get_env
from mgraph_ai_service_deploy.config                                                        import ENV_VAR__URL__TARGET_SERVER__GITHUB_SERVICE, ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_NAME, ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_VALUE
from mgraph_ai_service_deploy.schemas.auth.Schema__Auth__Config__External_Service           import Schema__Auth__Config__External_Service


class Auth__External_Services(Type_Safe):

    @cache_on_self
    def config__graph_service(self):
        key_name      = get_env(ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_NAME  )
        key_value     = get_env(ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_VALUE )
        target_server = get_env(ENV_VAR__URL__TARGET_SERVER__GITHUB_SERVICE             )
        with Schema__Auth__Config__External_Service() as _:
            if key_name and key_value and target_server:
                _.key_name      = key_name
                _.key_value     = key_value
                _.target_server = target_server
                _.enabled       = True
            return _

