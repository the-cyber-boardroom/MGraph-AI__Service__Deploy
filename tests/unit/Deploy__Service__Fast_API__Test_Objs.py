from typing                                                                                  import Tuple
from fastapi                                                                                 import FastAPI
from mgraph_ai_service_github.config import ENV_VAR__SERVICE__AUTH__PUBLIC_KEY, ENV_VAR__SERVICE__AUTH__PRIVATE_KEY
from mgraph_ai_service_github.fast_api.GitHub__Service__Fast_API                             import GitHub__Service__Fast_API
from mgraph_ai_service_github.service.encryption.NaCl__Key_Management import NaCl__Key_Management
from mgraph_ai_service_github.surrogates.github.testing.GitHub__API__Surrogate__Test_Context import GitHub__API__Surrogate__Test_Context
from osbot_fast_api.api.Fast_API                                                             import ENV_VAR__FAST_API__AUTH__API_KEY__NAME, ENV_VAR__FAST_API__AUTH__API_KEY__VALUE
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                         import Serverless__Fast_API__Config
from osbot_utils.type_safe.Type_Safe                                                         import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                        import Random_Guid
from osbot_utils.utils.Env                                                                   import set_env
from starlette.testclient                                                                    import TestClient
from mgraph_ai_service_deploy.fast_api.Deploy__Service__Fast_API                             import Deploy__Service__Fast_API
from mgraph_ai_service_deploy.services.Service__Public_Keys                                  import Service__Public_Keys
from mgraph_ai_service_deploy.services.Service__GitHub__Secrets                              import Service__GitHub__Secrets


TEST_API_KEY__NAME  = 'key-used-in-pytest'
TEST_API_KEY__VALUE = Random_Guid()


class Deploy__Service__Fast_API__Test_Objs(Type_Safe):
    fast_api                    : Deploy__Service__Fast_API              = None
    fast_api__app               : FastAPI                                = None
    fast_api__client            : TestClient                             = None
    github_service_client       : TestClient                             = None     # TestClient to local GitHub Service
    github_surrogate_context    : GitHub__API__Surrogate__Test_Context   = None     # Surrogate context for state control
    service_public_keys         : Service__Public_Keys                   = None     # Service with GitHub Service client
    service_github_secrets      : Service__GitHub__Secrets               = None     # Service with GitHub Service client
    setup_completed             : bool                                   = False


deploy_service_fast_api_test_objs = Deploy__Service__Fast_API__Test_Objs()          # Singleton instance


def setup__deploy_service__fast_api_test_objs():
    with deploy_service_fast_api_test_objs as _:
        if _.setup_completed is False:
            github_client, surrogate_ctx = create_github_service_test_client()       # Create local GitHub Service with surrogate
            _.github_service_client      = github_client
            _.github_surrogate_context   = surrogate_ctx
            _.service_public_keys        = Service__Public_Keys   (http_client=github_client)
            _.service_github_secrets     = Service__GitHub__Secrets(http_client=github_client)

            _.fast_api                   = Deploy__Service__Fast_API().setup()
            _.fast_api__app              = _.fast_api.app()
            _.fast_api__client           = _.fast_api.client()
            _.setup_completed            = True

            set_env(ENV_VAR__FAST_API__AUTH__API_KEY__NAME , TEST_API_KEY__NAME )
            set_env(ENV_VAR__FAST_API__AUTH__API_KEY__VALUE, TEST_API_KEY__VALUE)

    return deploy_service_fast_api_test_objs


def create_github_service_test_client() -> Tuple[TestClient, GitHub__API__Surrogate__Test_Context]:
    """Create local GitHub Service FastAPI app with surrogate backend.
    
    Returns TestClient pointing to real GitHub Service code, backed by in-memory surrogate.
    """
    create_and_set_nacl_keys()
    surrogate_context       = GitHub__API__Surrogate__Test_Context().setup()         # Setup surrogate FIRST
    serverless_config       = Serverless__Fast_API__Config(enable_api_key=False)     # Disable auth for tests
    github_service_fast_api = GitHub__Service__Fast_API(config=serverless_config).setup()
    fast_api_app            = github_service_fast_api.app()
    github_service_client   = TestClient(fast_api_app)

    return github_service_client, surrogate_context


def create_test_services() -> Tuple[Service__Public_Keys, Service__GitHub__Secrets, 
                                     TestClient, GitHub__API__Surrogate__Test_Context]:
    """Create services wired to local GitHub Service with surrogate backend."""
    github_client, surrogate_ctx = create_github_service_test_client()
    service_public_keys          = Service__Public_Keys   (http_client=github_client)
    service_github_secrets       = Service__GitHub__Secrets(http_client=github_client)
    return service_public_keys, service_github_secrets, github_client, surrogate_ctx


def reset_surrogate_state(surrogate_context: GitHub__API__Surrogate__Test_Context):
    """Reset surrogate state for test isolation."""
    if surrogate_context and surrogate_context.surrogate:
        surrogate_context.surrogate.state.reset()

def encrypt_pat_for_tests(github_client: TestClient, raw_pat: str) -> str:
    import base64
    from nacl.public import SealedBox, PublicKey

    response       = github_client.get('/encryption/public-key')
    public_key_hex = response.json()['public_key']
    pub_key_bytes  = bytes.fromhex(public_key_hex)
    nacl_pub_key   = PublicKey(pub_key_bytes)
    sealed_box     = SealedBox(nacl_pub_key)
    encrypted      = sealed_box.encrypt(raw_pat.encode())
    return base64.b64encode(encrypted).decode()


def create_and_set_nacl_keys():                                                         # Generate and set NaCl keys as environment variables
    nacl_manager = NaCl__Key_Management()
    nacl_keys    = nacl_manager.generate_nacl_keys()

    set_env(ENV_VAR__SERVICE__AUTH__PUBLIC_KEY , nacl_keys.public_key )
    set_env(ENV_VAR__SERVICE__AUTH__PRIVATE_KEY, nacl_keys.private_key)
    return nacl_keys