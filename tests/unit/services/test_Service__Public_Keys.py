from unittest                                                                                   import TestCase
from starlette.testclient                                                                       import TestClient
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Objects                                                                  import base_classes
from mgraph_ai_service_github.surrogates.github.testing.GitHub__API__Surrogate__Test_Context    import GitHub__API__Surrogate__Test_Context
from mgraph_ai_service_deploy.services.Service__Public_Keys                                     import Service__Public_Keys
from mgraph_ai_service_deploy.services.Service__GitHub__Secrets                                 import Service__GitHub__Secrets
from tests.unit.Deploy__Service__Fast_API__Test_Objs                                            import create_test_services


class test_Service__Public_Keys(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service_public_keys, cls.service_github_secrets, cls.github_client, cls.surrogate_context = create_test_services()

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

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                     # Test auto-initialization
        with Service__Public_Keys() as _:
            assert type(_)         is Service__Public_Keys
            assert base_classes(_) == [Type_Safe, object]
            assert 'github.dev.mgraph.ai' in str(_.github_service_url)
            assert _.request_timeout == 30
            assert _.http_client     is None                                    # Default is None (uses requests)

    def test__init__with_http_client(self):                                     # Test initialization with injected client
        with self.service_public_keys as _:
            assert type(_)         is Service__Public_Keys
            assert _.http_client   is not None
            assert _.http_client   is self.github_client

    # ═══════════════════════════════════════════════════════════════════════════════
    # get_github_public_key Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get_github_public_key(self):                                       # Test fetching public key via surrogate
        with self.service_public_keys as _:
            result = _.get_github_public_key()

            assert type(result)        is dict
            assert 'public_key'        in result
            assert 'algorithm'         in result
            assert 'service'           in result
            assert result['service']   == 'github'
            assert result['algorithm'] == 'NaCl/Curve25519/SealedBox'
            assert len(result['public_key']) == 64                              # 64 hex chars

    def test_get_github_public_key__returns_consistent_key(self):               # Test public key is consistent
        with self.service_public_keys as _:
            result_1 = _.get_github_public_key()
            result_2 = _.get_github_public_key()

            assert result_1['public_key'] == result_2['public_key']             # Same key each time

    # ═══════════════════════════════════════════════════════════════════════════════
    # get_public_key_for_service Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get_public_key_for_service__github(self):                          # Test getting key for github service
        with self.service_public_keys as _:
            result = _.get_public_key_for_service('github')

            assert result['service'] == 'github'
            assert 'public_key'      in result

    def test_get_public_key_for_service__unknown(self):                         # Test error for unknown service
        with self.service_public_keys as _:
            with self.assertRaises(ValueError) as context:
                _.get_public_key_for_service('unknown')

            assert "Unknown service: unknown" in str(context.exception)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_types__public_key_response(self):                                  # Test all field types in response
        with self.service_public_keys as _:
            result = _.get_github_public_key()

            assert type(result)               is dict
            assert type(result['public_key']) is str
            assert type(result['algorithm'])  is str
            assert type(result['service'])    is str