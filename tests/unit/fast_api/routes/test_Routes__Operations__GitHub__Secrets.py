from unittest                                                                                   import TestCase
from starlette.testclient                                                                       import TestClient
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Objects                                                                  import base_classes
from osbot_fast_api.api.routes.Fast_API__Routes                                                 import Fast_API__Routes
from mgraph_ai_service_github.surrogates.github.testing.GitHub__API__Surrogate__Test_Context    import GitHub__API__Surrogate__Test_Context
from mgraph_ai_service_deploy.fast_api.routes.Routes__Operations__GitHub__Secrets               import Routes__Operations__GitHub__Secrets
from mgraph_ai_service_deploy.fast_api.routes.Routes__Operations__GitHub__Secrets               import TAG__ROUTES_OPERATIONS_GITHUB_SECRETS
from mgraph_ai_service_deploy.fast_api.routes.Routes__Operations__GitHub__Secrets               import ROUTES_PATHS__OPERATIONS_GITHUB_SECRETS
from mgraph_ai_service_deploy.services.Service__Public_Keys                                     import Service__Public_Keys
from mgraph_ai_service_deploy.services.Service__GitHub__Secrets                                 import Service__GitHub__Secrets
from mgraph_ai_service_deploy.schemas.common.Schema__Response__Operation                        import Schema__Response__Operation
from mgraph_ai_service_deploy.schemas.common.Schema__Target__GitHub__Repo                       import Schema__Target__GitHub__Repo
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__List             import Schema__Request__GitHub__Secrets__List
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Get              import Schema__Request__GitHub__Secrets__Get
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Exists           import Schema__Request__GitHub__Secrets__Exists
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Create           import Schema__Request__GitHub__Secrets__Create
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Delete           import Schema__Request__GitHub__Secrets__Delete
from tests.unit.Deploy__Service__Fast_API__Test_Objs                                            import create_test_services, encrypt_pat_for_tests


class test_Routes__Operations__GitHub__Secrets(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service_public_keys, cls.service_github_secrets, cls.github_client, cls.surrogate_context = create_test_services()
        cls.routes     = Routes__Operations__GitHub__Secrets(service_github_secrets=cls.service_github_secrets)
        cls.test_owner = 'test-org'
        cls.test_repo  = 'test-repo'
        cls.encrypted_value = cls.encrypt_value('a_secret_value')

        cls.surrogate_context.add_repo(cls.test_owner, cls.test_repo)           # Add test repo to surrogate
        cls.raw_pat   = cls.surrogate_context.admin_pat()                       # Use admin PAT that works on surrogate
        cls.test_pat  = encrypt_pat_for_tests(cls.github_client, cls.raw_pat)

    @classmethod
    def tearDownClass(cls):
        if cls.surrogate_context:
            cls.surrogate_context.teardown()

    @classmethod
    def encrypt_value(cls, value: str) -> str:                                  # Helper to encrypt any value
        return encrypt_pat_for_tests(cls.github_client, value)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Setup Verification
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_setUpClass(self):
        assert type(self.service_public_keys   ) is Service__Public_Keys
        assert type(self.service_github_secrets) is Service__GitHub__Secrets
        assert type(self.github_client         ) is TestClient
        assert type(self.surrogate_context     ) is GitHub__API__Surrogate__Test_Context
        assert type(self.routes                ) is Routes__Operations__GitHub__Secrets

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                     # Test auto-initialization
        with Routes__Operations__GitHub__Secrets() as _:
            assert type(_)                         is Routes__Operations__GitHub__Secrets
            assert base_classes(_)                 == [Fast_API__Routes, Type_Safe, object]
            assert _.tag                           == TAG__ROUTES_OPERATIONS_GITHUB_SECRETS
            assert _.tag                           == 'operations/github/secrets'
            assert type(_.service_github_secrets)  is Service__GitHub__Secrets

    def test__tag_constant(self):                                               # Test tag constant
        assert TAG__ROUTES_OPERATIONS_GITHUB_SECRETS == 'operations/github/secrets'

    def test__routes_paths_constant(self):                                      # Test routes paths constant
        expected_paths = ['/operations/github/secrets/list'  ,
                          '/operations/github/secrets/get'    ,
                          '/operations/github/secrets/exists' ,
                          '/operations/github/secrets/create' ,
                          '/operations/github/secrets/delete' ]
        for path in expected_paths:
            assert path in ROUTES_PATHS__OPERATIONS_GITHUB_SECRETS

    def test__service_dependency(self):                                         # Test service is injected
        with self.routes as _:
            assert _.service_github_secrets is not None
            assert type(_.service_github_secrets) is Service__GitHub__Secrets
            assert _.service_github_secrets       is self.service_github_secrets

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def create_target(self):                                                    # Helper to create repo target
        return Schema__Target__GitHub__Repo(owner = self.test_owner,
                                            repo  = self.test_repo )

    def create_secret_via_route(self, secret_name: str):                        # Helper to create secret via route
        request = Schema__Request__GitHub__Secrets__Create(
            encrypted_pat   = self.test_pat         ,
            target          = self.create_target()  ,
            secret_name     = secret_name           ,
            encrypted_value = self.encrypted_value  )
        return self.routes.create(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__list_method_signature(self):                                      # Test list method exists
        with Routes__Operations__GitHub__Secrets() as _:
            assert hasattr(_, 'list')
            assert callable(_.list)

            import inspect
            sig    = inspect.signature(_.list)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Request__GitHub__Secrets__List
            assert sig.return_annotation == Schema__Response__Operation

    def test__get_method_signature(self):                                       # Test get method exists
        with Routes__Operations__GitHub__Secrets() as _:
            assert hasattr(_, 'get')
            assert callable(_.get)

            import inspect
            sig    = inspect.signature(_.get)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Request__GitHub__Secrets__Get

    def test__exists_method_signature(self):                                    # Test exists method exists
        with Routes__Operations__GitHub__Secrets() as _:
            assert hasattr(_, 'exists')
            assert callable(_.exists)

            import inspect
            sig    = inspect.signature(_.exists)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Request__GitHub__Secrets__Exists

    def test__create_method_signature(self):                                    # Test create method exists
        with Routes__Operations__GitHub__Secrets() as _:
            assert hasattr(_, 'create')
            assert callable(_.create)

            import inspect
            sig    = inspect.signature(_.create)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Request__GitHub__Secrets__Create

    def test__delete_method_signature(self):                                    # Test delete method exists
        with Routes__Operations__GitHub__Secrets() as _:
            assert hasattr(_, 'delete')
            assert callable(_.delete)

            import inspect
            sig    = inspect.signature(_.delete)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Request__GitHub__Secrets__Delete

    # ═══════════════════════════════════════════════════════════════════════════════
    # Route Method Tests - list
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_list(self):                                                        # Test list route method
        request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat      ,
                                                         target        = self.create_target())

        with self.routes as _:
            result = _.list(request)

            assert type(result)     is Schema__Response__Operation
            assert result.success   is True
            assert result.operation == 'github:secrets:list'
            assert 'secrets'        in result.data

    def test_list__with_secrets(self):                                          # Test list after creating secrets
        self.create_secret_via_route('LIST_TEST_1')
        self.create_secret_via_route('LIST_TEST_2')

        request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat      ,
                                                         target        = self.create_target())

        with self.routes as _:
            result = _.list(request)

            assert result.success is True
            secret_names = [s['name'] for s in result.data['secrets']]
            assert 'LIST_TEST_1' in secret_names
            assert 'LIST_TEST_2' in secret_names

    # ═══════════════════════════════════════════════════════════════════════════════
    # Route Method Tests - get
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get__exists(self):                                                 # Test get route for existing secret
        self.create_secret_via_route('GET_TEST')

        request = Schema__Request__GitHub__Secrets__Get(encrypted_pat = self.test_pat       ,
                                                        target        = self.create_target(),
                                                        secret_name   = 'GET_TEST'          )

        with self.routes as _:
            result = _.get(request)

            assert result.success   is True
            assert result.operation == 'github:secrets:get'
            assert 'secret'         in result.data
            assert result.data['secret']['name'] == 'GET_TEST'

    def test_get__not_exists(self):                                             # Test get route for non-existent secret
        request = Schema__Request__GitHub__Secrets__Get(encrypted_pat = self.test_pat        ,
                                                        target        = self.create_target() ,
                                                        secret_name   = 'NONEXISTENT_GET'    )

        with self.routes as _:
            result = _.get(request)

            assert result.success is False
            assert result.error   is not None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Route Method Tests - exists
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_exists__true(self):                                                # Test exists route for existing secret
        self.create_secret_via_route('EXISTS_TEST')

        request = Schema__Request__GitHub__Secrets__Exists(encrypted_pat = self.test_pat       ,
                                                           target        = self.create_target(),
                                                           secret_name   = 'EXISTS_TEST'       )

        with self.routes as _:
            result = _.exists(request)

            assert result.success        is True
            assert result.operation      == 'github:secrets:exists'
            assert result.data['exists'] is True

    def test_exists__false(self):                                               # Test exists route for non-existent secret
        request = Schema__Request__GitHub__Secrets__Exists(encrypted_pat = self.test_pat         ,
                                                           target        = self.create_target()  ,
                                                           secret_name   = 'NONEXISTENT_EXISTS'  )

        with self.routes as _:
            result = _.exists(request)

            assert result.success        is True                                # Operation succeeded
            assert result.data['exists'] is False                               # Secret doesn't exist

    # ═══════════════════════════════════════════════════════════════════════════════
    # Route Method Tests - create
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_create(self):                                                      # Test create route method
        request = Schema__Request__GitHub__Secrets__Create(
            encrypted_pat   = self.test_pat        ,
            target          = self.create_target() ,
            secret_name     = 'NEW_SECRET'         ,
            encrypted_value = self.encrypted_value )

        with self.routes as _:
            result = _.create(request)

            assert result.success   is True
            assert result.operation == 'github:secrets:create'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Route Method Tests - delete
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_delete__exists(self):                                              # Test delete route for existing secret
        self.create_secret_via_route('TO_DELETE')

        request = Schema__Request__GitHub__Secrets__Delete(encrypted_pat = self.test_pat       ,
                                                           target        = self.create_target(),
                                                           secret_name   = 'TO_DELETE'         )

        with self.routes as _:
            result = _.delete(request)

            assert result.success   is True
            assert result.operation == 'github:secrets:delete'

    def test_delete__not_exists(self):                                          # Test delete route for non-existent secret
        request = Schema__Request__GitHub__Secrets__Delete(encrypted_pat = self.test_pat          ,
                                                           target        = self.create_target()   ,
                                                           secret_name   = 'NONEXISTENT_DELETE'   )

        with self.routes as _:
            result = _.delete(request)

            assert result.success is False                                      # Secret not found

    # ═══════════════════════════════════════════════════════════════════════════════
    # setup_routes Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__setup_routes(self):                                               # Test setup_routes method
        from fastapi import FastAPI
        with Routes__Operations__GitHub__Secrets(app=FastAPI()) as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)

            result = _.setup_routes()
            assert result is _                                                  # Returns self for chaining

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_types__response(self):                                             # Test response types for all methods
        request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat      ,
                                                         target        = self.create_target())

        with self.routes as _:
            result = _.list(request)

            assert type(result)          is Schema__Response__Operation
            assert type(result.success)  is bool

    # ═══════════════════════════════════════════════════════════════════════════════
    # Surrogate State Verification Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_surrogate__verify_create_updates_state(self):                      # Test create updates surrogate state
        self.create_secret_via_route('STATE_VERIFY')

        state  = self.surrogate_context.surrogate.state
        secret = state.get_repo_secret(self.test_owner, self.test_repo, 'STATE_VERIFY')

        assert secret      is not None
        assert secret.name == 'STATE_VERIFY'

    # ═══════════════════════════════════════════════════════════════════════════════
    # End-to-End Flow Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_flow__crud_via_routes(self):                                       # Test complete CRUD flow via routes
        with self.routes as _:
            target = self.create_target()

            # Create
            create_request = Schema__Request__GitHub__Secrets__Create(encrypted_pat   = self.test_pat        ,
                                                                      target          = target               ,
                                                                      secret_name     = 'FLOW_TEST'          ,
                                                                      encrypted_value = self.encrypted_value )
            create_result = _.create(create_request)
            assert create_result.success is True

            # Exists
            exists_request = Schema__Request__GitHub__Secrets__Exists(encrypted_pat = self.test_pat   ,
                                                                      target        = target          ,
                                                                      secret_name   = 'FLOW_TEST'     )
            exists_result = _.exists(exists_request)
            assert exists_result.data['exists'] is True

            # Get
            get_request = Schema__Request__GitHub__Secrets__Get(encrypted_pat = self.test_pat   ,
                                                                target        = target          ,
                                                                secret_name   = 'FLOW_TEST'     )
            get_result = _.get(get_request)
            assert get_result.success is True

            # List
            list_request = Schema__Request__GitHub__Secrets__List(encrypted_pat = self.test_pat,
                                                                  target        = target       )
            list_result  = _.list(list_request)
            secret_names = [s['name'] for s in list_result.data['secrets']]
            assert 'FLOW_TEST' in secret_names

            # Verify via surrogate state
            state = self.surrogate_context.surrogate.state
            assert state.get_repo_secret(self.test_owner, self.test_repo, 'FLOW_TEST') is not None

            # Delete
            delete_request = Schema__Request__GitHub__Secrets__Delete(encrypted_pat = self.test_pat   ,
                                                                      target        = target          ,
                                                                      secret_name   = 'FLOW_TEST'     )
            delete_result  = _.delete(delete_request)
            assert delete_result.success is True

            # Verify deleted
            exists_after = _.exists(exists_request)
            assert exists_after.data['exists'] is False

            # Verify via surrogate state
            assert state.get_repo_secret(self.test_owner, self.test_repo, 'FLOW_TEST') is None