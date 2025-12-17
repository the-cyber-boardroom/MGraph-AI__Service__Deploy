from unittest                                                                                   import TestCase
from starlette.testclient                                                                       import TestClient
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Objects                                                                  import base_classes
from osbot_fast_api.api.routes.Fast_API__Routes                                                 import Fast_API__Routes
from mgraph_ai_service_github.surrogates.github.testing.GitHub__API__Surrogate__Test_Context    import GitHub__API__Surrogate__Test_Context
from mgraph_ai_service_deploy.fast_api.routes.Routes__Public_Keys                               import Routes__Public_Keys
from mgraph_ai_service_deploy.fast_api.routes.Routes__Public_Keys                               import TAG__ROUTES_PUBLIC_KEYS, ROUTES_PATHS__PUBLIC_KEYS
from mgraph_ai_service_deploy.services.Service__Public_Keys                                     import Service__Public_Keys
from mgraph_ai_service_deploy.services.Service__GitHub__Secrets                                 import Service__GitHub__Secrets
from tests.unit.Deploy__Service__Fast_API__Test_Objs                                            import create_test_services


class test_Routes__Public_Keys(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service_public_keys, cls.service_github_secrets, cls.github_client, cls.surrogate_context = create_test_services()
        cls.routes = Routes__Public_Keys(service_public_keys=cls.service_public_keys)

    @classmethod
    def tearDownClass(cls):
        if cls.surrogate_context:
            cls.surrogate_context.teardown()

    # ═══════════════════════════════════════════════════════════════════════════════
    # Setup Verification
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_setUpClass(self):
        assert type(self.service_public_keys   ) is Service__Public_Keys
        assert type(self.service_github_secrets) is Service__GitHub__Secrets
        assert type(self.github_client         ) is TestClient
        assert type(self.surrogate_context     ) is GitHub__API__Surrogate__Test_Context
        assert type(self.routes                ) is Routes__Public_Keys

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                     # Test auto-initialization
        with Routes__Public_Keys() as _:
            assert type(_)                     is Routes__Public_Keys
            assert base_classes(_)             == [Fast_API__Routes, Type_Safe, object]
            assert _.tag                       == TAG__ROUTES_PUBLIC_KEYS
            assert _.tag                       == 'public-keys'
            assert type(_.service_public_keys) is Service__Public_Keys

    def test__tag_constant(self):                                               # Test tag constant
        assert TAG__ROUTES_PUBLIC_KEYS == 'public-keys'

    def test__routes_paths_constant(self):                                      # Test routes paths constant
        assert '/public-keys/github' in ROUTES_PATHS__PUBLIC_KEYS

    def test__service_dependency(self):                                         # Test service is injected
        with self.routes as _:
            assert _.service_public_keys is not None
            assert type(_.service_public_keys) is Service__Public_Keys
            assert _.service_public_keys       is self.service_public_keys      # Same instance as setup

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__github_method_signature(self):                                    # Test github method exists
        with Routes__Public_Keys() as _:
            assert hasattr(_, 'github')
            assert callable(_.github)

            import inspect
            sig    = inspect.signature(_.github)
            params = list(sig.parameters.values())
            assert len(params)           == 0                                   # No parameters
            assert sig.return_annotation is not inspect.Parameter.empty

    # ═══════════════════════════════════════════════════════════════════════════════
    # Route Method Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_github(self):                                                      # Test github route method
        with self.routes as _:
            result = _.github()

            assert type(result)        is dict
            assert 'public_key'        in result
            assert 'algorithm'         in result
            assert 'service'           in result
            assert result['service']   == 'github'
            assert result['algorithm'] == 'NaCl/Curve25519/SealedBox'

    # ═══════════════════════════════════════════════════════════════════════════════
    # setup_routes Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__setup_routes(self):                                               # Test setup_routes method
        from fastapi import FastAPI
        with Routes__Public_Keys(app=FastAPI()) as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)

            result = _.setup_routes()
            assert result is _                                                  # Returns self for chaining

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_types__github_response(self):                                      # Test response type
        with self.routes as _:
            result = _.github()

            assert type(result)               is dict
            assert type(result['public_key']) is str
            assert type(result['algorithm'])  is str
            assert type(result['service'])    is str