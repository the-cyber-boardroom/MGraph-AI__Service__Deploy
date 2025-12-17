from unittest                                                                                   import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Float                                           import Safe_Float
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label              import Safe_Str__Label
from mgraph_ai_service_github.surrogates.github.testing.GitHub__API__Surrogate__Test_Context    import GitHub__API__Surrogate__Test_Context
from osbot_utils.testing.__                                                                     import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                            import Safe_UInt
from osbot_utils.utils.Objects                                                                  import base_classes
from starlette.testclient                                                                       import TestClient
from mgraph_ai_service_deploy.services.Service__Public_Keys                                     import Service__Public_Keys
from mgraph_ai_service_deploy.services.Service__GitHub__Secrets                                 import Service__GitHub__Secrets
from mgraph_ai_service_deploy.schemas.common.Schema__Rate_Limit                                 import Schema__Rate_Limit
from mgraph_ai_service_deploy.schemas.common.Schema__Response__Operation                        import Schema__Response__Operation
from mgraph_ai_service_deploy.schemas.common.Schema__Target__GitHub__Repo                       import Schema__Target__GitHub__Repo
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__List             import Schema__Request__GitHub__Secrets__List
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Get              import Schema__Request__GitHub__Secrets__Get
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Exists           import Schema__Request__GitHub__Secrets__Exists
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Create           import Schema__Request__GitHub__Secrets__Create
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Delete           import Schema__Request__GitHub__Secrets__Delete
from tests.unit.Deploy__Service__Fast_API__Test_Objs                                            import create_test_services, encrypt_pat_for_tests


class test_Service__GitHub__Secrets(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service_public_keys, cls.service_github_secrets, cls.github_client, cls.surrogate_context = create_test_services()
        cls.test_owner = 'test-org'
        cls.test_repo  = 'test-repo'
        cls.encrypted_value = cls.encrypt_value('an_value')

        cls.surrogate_context.add_repo(cls.test_owner, cls.test_repo)        # Add test repo to surrogate
        cls.raw_pat   = cls.surrogate_context.admin_pat()                      # use an admin PAT that works on the surrogate
        cls.test_pat  = encrypt_pat_for_tests(cls.github_client, cls.raw_pat)

    @classmethod
    def tearDownClass(cls):
        if cls.surrogate_context:
            cls.surrogate_context.teardown()

    # def setUp(self):
    #     #reset_surrogate_state(self.surrogate_context)                           # Reset surrogate state before each test
    #     #


    @classmethod
    def encrypt_value(cls, value: str) -> str:                                 # Helper to encrypt any value
        return encrypt_pat_for_tests(cls.github_client, value)
    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_setUpClass(self):
        assert type(self.service_public_keys    ) is Service__Public_Keys
        assert type(self.github_client          ) is TestClient
        assert type(self.service_github_secrets ) is Service__GitHub__Secrets
        assert type(self.surrogate_context      ) is GitHub__API__Surrogate__Test_Context

    def test__init__(self):                                                     # Test auto-initialization
        with Service__GitHub__Secrets() as _:
            assert type(_)         is Service__GitHub__Secrets
            assert base_classes(_) == [Type_Safe, object]
            assert 'github.dev.mgraph.ai' in str(_.github_service_url)
            assert _.request_timeout == 30
            assert _.http_client     is None                                    # Default is None (uses requests)
            assert _.obj()           == __(github_service_url     ='https://github.dev.mgraph.ai' ,
                                           request_timeout        = 30                            ,
                                           http_client            = None                          ,
                                           auth_external_services = __()                          )

    def test__init__with_http_client(self):                                     # Test initialization with injected client
        with self.service_github_secrets as _:
            assert type(_)       is Service__GitHub__Secrets
            assert _.http_client is not None
            assert _.http_client is self.github_client

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def create_target(self):                                                    # Helper to create repo target
        return Schema__Target__GitHub__Repo(owner = self.test_owner,
                                            repo  = self.test_repo )

    def create_secret(self, secret_name: str, secret_value: str = 'test-secret-value'):  # Helper to create a secret
        encrypted_value = self.encrypt_value(secret_value)                               # Encrypt the secret value
        request = Schema__Request__GitHub__Secrets__Create(
            encrypted_pat   = self.test_pat          ,
            target          = self.create_target()   ,
            secret_name     = secret_name            ,
            encrypted_value = encrypted_value        )
        return self.service_github_secrets.create_secret(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # list_secrets Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__list_secrets__empty_repo(self):                                    # Test listing secrets in empty repo

        request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat      ,
                                                         target        = self.create_target())


        with self.service_github_secrets as _:
            result = _.list_secrets(request)

            assert type(result)           is Schema__Response__Operation
            assert result.success         is True
            assert result.operation       == 'github:secrets:list'
            assert result.data            is not None
            assert 'secrets'              in result.data
            assert result.data['secrets'] == []                                 # Empty repo

    def test_list_secrets__with_secrets(self):                                  # Test listing secrets after creating some
        self.create_secret('AWS_ACCESS_KEY_ID')
        self.create_secret('AWS_SECRET_ACCESS_KEY')

        request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat      ,
                                                         target        = self.create_target())

        with self.service_github_secrets as _:
            result = _.list_secrets(request)

            assert result.success is True
            assert len(result.data['secrets']) == 7

            secret_names = [s['name'] for s in result.data['secrets']]
            assert 'AWS_ACCESS_KEY_ID'     in secret_names
            assert 'AWS_SECRET_ACCESS_KEY' in secret_names

    # ═══════════════════════════════════════════════════════════════════════════════
    # get_secret Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get_secret__exists(self):                                          # Test getting existing secret
        self.create_secret('MY_SECRET')

        request = Schema__Request__GitHub__Secrets__Get(encrypted_pat = self.test_pat       ,
                                                        target        = self.create_target(),
                                                        secret_name   = 'MY_SECRET'         )

        with self.service_github_secrets as _:
            result = _.get_secret(request)

            assert result.success   is True
            assert result.operation == 'github:secrets:get'
            assert 'secret'         in result.data
            assert result.data['secret']['name'] == 'MY_SECRET'

    def test_get_secret__not_exists(self):                                      # Test getting non-existent secret
        request = Schema__Request__GitHub__Secrets__Get(encrypted_pat = self.test_pat        ,
                                                        target        = self.create_target() ,
                                                        secret_name   = 'NONEXISTENT'        )

        with self.service_github_secrets as _:
            result = _.get_secret(request)

            assert result.success is False
            assert result.error   is not None
            assert 'not found'    in result.error.lower()

    # ═══════════════════════════════════════════════════════════════════════════════
    # secret_exists Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_secret_exists__true(self):                                         # Test exists check for existing secret
        self.create_secret('EXISTING_SECRET')

        request = Schema__Request__GitHub__Secrets__Exists(encrypted_pat = self.test_pat        ,
                                                           target        = self.create_target() ,
                                                           secret_name   = 'EXISTING_SECRET'    )

        with self.service_github_secrets as _:
            result = _.secret_exists(request)

            assert result.success             is True                           # Operation succeeded
            assert result.operation           == 'github:secrets:exists'
            assert result.data['exists']      is True                           # Secret exists
            assert result.data['secret_name'] == 'EXISTING_SECRET'

    def test_secret_exists__false(self):                                        # Test exists check for non-existent secret
        request = Schema__Request__GitHub__Secrets__Exists(encrypted_pat = self.test_pat       ,
                                                           target        = self.create_target(),
                                                           secret_name   = 'NONEXISTENT'       )

        with self.service_github_secrets as _:
            result = _.secret_exists(request)

            assert result.success        is True                                # Operation succeeded
            assert result.data['exists'] is False                               # Secret does NOT exist

    # ═══════════════════════════════════════════════════════════════════════════════
    # create_secret Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_create_secret(self):                                               # Test creating new secret

        request         = Schema__Request__GitHub__Secrets__Create(
            encrypted_pat   = self.test_pat                 ,
            target          = self.create_target()          ,
            secret_name     = 'NEW_SECRET'                  ,
            encrypted_value = self.encrypted_value          )

        with self.service_github_secrets as _:
            result = _.create_secret(request)

            assert result.success   is True
            assert result.operation == 'github:secrets:create'

            # Verify by listing
            list_request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat      ,
                                                                   target        = self.create_target())
            list_result  = _.list_secrets(list_request)

            secret_names = [s['name'] for s in list_result.data['secrets']]
            assert 'NEW_SECRET' in secret_names

    def test_create_secret__update_existing(self):                              # Test updating existing secret
        self.create_secret('UPDATABLE_SECRET')

        request = Schema__Request__GitHub__Secrets__Create(
            encrypted_pat   = self.test_pat              ,
            target          = self.create_target()       ,
            secret_name     = 'UPDATABLE_SECRET'         ,
            encrypted_value = self.encrypted_value       )               # New value

        with self.service_github_secrets as _:
            result = _.create_secret(request)

            assert result.success is True                                       # Update succeeds

    # ═══════════════════════════════════════════════════════════════════════════════
    # delete_secret Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_delete_secret__exists(self):                                       # Test deleting existing secret
        self.create_secret('TO_DELETE')

        request = Schema__Request__GitHub__Secrets__Delete(encrypted_pat = self.test_pat  ,
                                                           target        = self.create_target(),
                                                           secret_name   = 'TO_DELETE'    )

        with self.service_github_secrets as _:
            result = _.delete_secret(request)

            assert result.success   is True
            assert result.operation == 'github:secrets:delete'

            # Verify secret was deleted by listing
            list_request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat      ,
                                                                   target        = self.create_target())
            list_result  = _.list_secrets(list_request)

            secret_names = [s['name'] for s in list_result.data['secrets']]
            assert 'TO_DELETE' not in secret_names

    def test_delete_secret__not_exists(self):                                   # Test deleting non-existent secret
        request = Schema__Request__GitHub__Secrets__Delete(encrypted_pat = self.test_pat       ,
                                                           target        = self.create_target(),
                                                           secret_name   = 'NONEXISTENT'       )

        with self.service_github_secrets as _:
            result = _.delete_secret(request)

            assert result.success is False                                       # Operation succeeded (idempotent)
            assert result.obj()   == __(success   =  False,
                                        operation = 'github:secrets:delete',
                                        data      = __(),
                                        error     = "Secret 'NONEXISTENT' not found or could not be deleted",
                                        duration  = __SKIP__,
                                        rate_limit= __(remaining=4999, limit=5000, timestamp_reset=0, used=1))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Request Transform Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_transform_list_request(self):                                      # Test list request transformation
        request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat      ,
                                                         target        = self.create_target())

        with self.service_github_secrets as _:
            result = _.transform_list_request(request)

            assert type(result)                  is dict
            assert result['encrypted_pat']       == self.test_pat
            assert result['request_data']['owner'] == self.test_owner
            assert result['request_data']['repo']  == self.test_repo

    def test_transform_create_request(self):                                    # Test create request transformation
        request = Schema__Request__GitHub__Secrets__Create(
            encrypted_pat   = self.test_pat                 ,
            target          = self.create_target()          ,
            secret_name     = 'TEST_SECRET'                 ,
            encrypted_value = 'RW5jcnlwdGVkVmFsdWU='        )

        with self.service_github_secrets as _:
            result = _.transform_create_request(request)

            assert result['request_data']['secret_name']     == 'TEST_SECRET'
            assert result['request_data']['encrypted_value'] == 'RW5jcnlwdGVkVmFsdWU='

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_types__response_operation(self):                                   # Test response types
        request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat      ,
                                                         target        = self.create_target())

        with self.service_github_secrets as _:
            result = _.list_secrets(request)

            assert type(result)            is Schema__Response__Operation
            assert type(result.success)    is bool
            assert type(result.operation)  is Safe_Str__Label
            assert type(result.duration)   is Safe_Float
            assert type(result.rate_limit) is Schema__Rate_Limit

    def test_types__rate_limit(self):                                           # Test rate limit types
        request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat      ,
                                                         target        = self.create_target())

        with self.service_github_secrets as _:
            result = _.list_secrets(request)

            assert result.rate_limit is not None
            assert type(result.rate_limit.remaining) is Safe_UInt
            assert type(result.rate_limit.limit)     is Safe_UInt
            assert result.rate_limit.limit           == 5000

    # ═══════════════════════════════════════════════════════════════════════════════
    # Surrogate State Inspection Tests (NEW - testing surrogate directly)
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_surrogate__state_inspection(self):                                 # Test inspecting surrogate state directly
        self.create_secret('INSPECTABLE_SECRET')

        state  = self.surrogate_context.surrogate.state
        secret = state.get_repo_secret(self.test_owner, self.test_repo, 'INSPECTABLE_SECRET')

        assert secret          is not None
        assert secret.name     == 'INSPECTABLE_SECRET'

    def test_surrogate__list_secrets_via_state(self):                           # Test listing secrets via state
        self.create_secret('STATE_SECRET_1')
        self.create_secret('STATE_SECRET_2')

        state   = self.surrogate_context.surrogate.state
        secrets = state.list_repo_secrets(self.test_owner, self.test_repo)

        assert len(secrets) == 10
        secret_names = [s.name for s in secrets]
        assert 'STATE_SECRET_1' in secret_names
        assert 'STATE_SECRET_2' in secret_names

    # ═══════════════════════════════════════════════════════════════════════════════
    # End-to-End Flow Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_flow__create_list_delete(self):                                    # Test complete CRUD flow
        with self.service_github_secrets as _:
            target = self.create_target()

            # Create secrets
            for name in ['SECRET_1', 'SECRET_2', 'SECRET_3']:
                create_req = Schema__Request__GitHub__Secrets__Create(encrypted_pat   = self.test_pat         ,
                                                                      target          = target                ,
                                                                      secret_name     = name                  ,
                                                                      encrypted_value = self.encrypted_value  )
                create_result = _.create_secret(create_req)
                assert create_result.success is True

            # List and verify
            list_req    = Schema__Request__GitHub__Secrets__List(encrypted_pat=self.test_pat, target=target)
            list_result = _.list_secrets(list_req)
            assert len(list_result.data['secrets']) == 5

            # Delete one
            delete_req    = Schema__Request__GitHub__Secrets__Delete(encrypted_pat=self.test_pat, target=target, secret_name='SECRET_2')
            delete_result = _.delete_secret(delete_req)
            assert delete_result.success is True

            # Verify deletion
            list_result = _.list_secrets(list_req)
            assert len(list_result.data['secrets']) == 4
            secret_names = [s['name'] for s in list_result.data['secrets']]
            assert 'SECRET_2' not in secret_names

            # Also verify via surrogate state
            state   = self.surrogate_context.surrogate.state
            secrets = state.list_repo_secrets(self.test_owner, self.test_repo)
            assert len(secrets) == 4
