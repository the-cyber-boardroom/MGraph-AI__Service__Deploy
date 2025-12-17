import pytest
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url            import Safe_Str__Url
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.utils.Env                                                          import get_env
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from mgraph_ai_service_deploy.config                                                import ENV_VAR__DEPLOY_SERVICE__URL, ENV_VAR__DEPLOY_SERVICE__API_KEY__NAME, ENV_VAR__DEPLOY_SERVICE__API_KEY__VALUE, ENV_VAR__GIT_HUB__ACCESS_TOKEN
from mgraph_ai_service_deploy.utils.testing.QA__Deploy_Service_Client               import QA__Deploy_Service_Client
from mgraph_ai_service_deploy.utils.testing.QA__HTTP_Client__Deploy_Service         import QA__HTTP_Client__Deploy_Service


class QA__Test_Objs(Type_Safe):                                                     # Shared test objects for QA tests
    deploy_client   : QA__Deploy_Service_Client = None
    setup_completed : bool                      = False
    setup_error     : str                       = None


qa_test_objs = QA__Test_Objs()                                                      # Singleton instance



def setup__qa_test_objs() -> QA__Test_Objs:                                         # Initialize QA test objects from environment
    with qa_test_objs as _:
        if _.setup_completed:
            return _

        service_url   = get_env(ENV_VAR__DEPLOY_SERVICE__URL           , '')
        api_key_name  = get_env(ENV_VAR__DEPLOY_SERVICE__API_KEY__NAME , '')
        api_key_value = get_env(ENV_VAR__DEPLOY_SERVICE__API_KEY__VALUE, '')
        github_pat    = get_env(ENV_VAR__GIT_HUB__ACCESS_TOKEN         , '')

        if service_url and api_key_name and api_key_value and github_pat:
            http_client = QA__HTTP_Client__Deploy_Service(service_url   = Safe_Str__Url (service_url  )                    ,
                                                          api_key_name  = Safe_Str__Text(api_key_name ) if api_key_name  else None,
                                                          api_key_value = Safe_Str__Text(api_key_value) if api_key_value else None)
        else:
            raise Exception("[in setup__qa_test_objs] api_key_name and api_key_value are required")

        _.deploy_client = QA__Deploy_Service_Client(http_client = http_client ,
                                                    github_pat  = github_pat  )

        _.setup_completed = True

    return qa_test_objs


# ═══════════════════════════════════════════════════════════════════════════════════
# Skip Decorators for Tests
# ═══════════════════════════════════════════════════════════════════════════════════

def skip_if_no_deploy_service():                                                    # Skip if Deploy Service URL not configured
    service_url = get_env(ENV_VAR__DEPLOY_SERVICE__URL, '')
    if not service_url:
        pytest.skip(f"QA tests require {ENV_VAR__DEPLOY_SERVICE__URL} to be set")


def skip_if_no_github_pat():                                                        # Skip if GitHub PAT not configured
    github_pat = get_env(ENV_VAR__GIT_HUB__ACCESS_TOKEN, '')
    if not github_pat:
        pytest.skip(f"GitHub PAT tests require {ENV_VAR__GIT_HUB__ACCESS_TOKEN} to be set")


def skip_if_no_api_key():                                                           # Skip if API key not configured
    api_key_value = get_env(ENV_VAR__DEPLOY_SERVICE__API_KEY__VALUE, '')
    if not api_key_value:
        pytest.skip(f"API key tests require {ENV_VAR__DEPLOY_SERVICE__API_KEY__VALUE} to be set")