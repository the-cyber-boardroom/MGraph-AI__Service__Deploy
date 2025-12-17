# todo: fix these tests
#       and see if integration is best location for them
#       and if test_Deploy__Service__Fast_API__Client is the best name to use
# from unittest                                                                                   import TestCase
# from starlette.testclient                                                                       import TestClient
# from mgraph_ai_service_github.surrogates.github.testing.GitHub__API__Surrogate__Test_Context    import GitHub__API__Surrogate__Test_Context
# from mgraph_ai_service_deploy.fast_api.routes.Routes__Public_Keys                               import ROUTES_PATHS__PUBLIC_KEYS
# from mgraph_ai_service_deploy.fast_api.routes.Routes__Operations__GitHub__Secrets               import ROUTES_PATHS__OPERATIONS_GITHUB_SECRETS
# from mgraph_ai_service_deploy.fast_api.Deploy__Service__Fast_API                                import Deploy__Service__Fast_API
# from tests.unit.Deploy__Service__Fast_API__Test_Objs                                            import setup__deploy_service__fast_api_test_objs
# from tests.unit.Deploy__Service__Fast_API__Test_Objs                                            import TEST_API_KEY__NAME, TEST_API_KEY__VALUE
# from tests.unit.Deploy__Service__Fast_API__Test_Objs                                            import encrypt_pat_for_tests
#
#
# class test_Deploy__Service__Fast_API__Client(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         cls.test_objs = setup__deploy_service__fast_api_test_objs()
#         with cls.test_objs as _:
#             cls.client               = _.fast_api__client
#             cls.fast_api             = _.fast_api
#             cls.surrogate_context    = _.github_surrogate_context
#             cls.github_service_client = _.github_service_client
#             cls.headers              = {TEST_API_KEY__NAME: TEST_API_KEY__VALUE}
#             cls.test_owner           = 'test-org'
#             cls.test_repo            = 'test-repo'
#             cls.encrypted_value      = cls.encrypt_value('a_secret_value')
#
#             cls.surrogate_context.add_repo(cls.test_owner, cls.test_repo)        # Add test repo to surrogate
#             cls.raw_pat  = cls.surrogate_context.admin_pat()                     # Use admin PAT that works on surrogate
#             cls.test_pat = encrypt_pat_for_tests(cls.github_service_client, cls.raw_pat)
#
#     @classmethod
#     def tearDownClass(cls):
#         if cls.surrogate_context:
#             cls.surrogate_context.teardown()
#
#     @classmethod
#     def encrypt_value(cls, value: str) -> str:                                   # Helper to encrypt any value
#         return encrypt_pat_for_tests(cls.github_service_client, value)
#
#     # ═══════════════════════════════════════════════════════════════════════════════
#     # Setup Verification
#     # ═══════════════════════════════════════════════════════════════════════════════
#
#     def test_setUpClass(self):
#         assert type(self.client             ) is TestClient
#         assert type(self.fast_api           ) is Deploy__Service__Fast_API
#         assert type(self.surrogate_context  ) is GitHub__API__Surrogate__Test_Context
#         assert type(self.github_service_client) is TestClient
#
#     # ═══════════════════════════════════════════════════════════════════════════════
#     # Routes Registration Tests
#     # ═══════════════════════════════════════════════════════════════════════════════
#
#     def test__routes_registered(self):                                          # Test all routes are registered
#         routes = self.fast_api.routes_paths()
#
#         for path in ROUTES_PATHS__PUBLIC_KEYS:
#             assert path in routes, f"Missing route: {path}"
#
#         for path in ROUTES_PATHS__OPERATIONS_GITHUB_SECRETS:
#             assert path in routes, f"Missing route: {path}"
#
#     # ═══════════════════════════════════════════════════════════════════════════════
#     # Auth Tests
#     # ═══════════════════════════════════════════════════════════════════════════════
#
#     def test__auth_required(self):                                              # Test auth is required
#         response = self.client.get('/public-keys/github')                       # No auth headers
#         assert response.status_code == 401
#
#     def test__auth_succeeds(self):                                              # Test auth succeeds with correct key
#         response = self.client.get('/public-keys/github', headers=self.headers)
#         assert response.status_code == 200
#
#     # ═══════════════════════════════════════════════════════════════════════════════
#     # Public Keys Endpoint Tests
#     # ═══════════════════════════════════════════════════════════════════════════════
#
#     def test__public_keys_github(self):                                         # Test GET /public-keys/github
#         response = self.client.get('/public-keys/github', headers=self.headers)
#
#         assert response.status_code == 200
#         data = response.json()
#         assert 'public_key' in data
#         assert 'algorithm'  in data
#         assert 'service'    in data
#         assert data['service']   == 'github'
#         assert data['algorithm'] == 'NaCl/Curve25519/SealedBox'
#
#     # ═══════════════════════════════════════════════════════════════════════════════
#     # GitHub Secrets - List Tests
#     # ═══════════════════════════════════════════════════════════════════════════════
#
#     def test__operations_github_secrets_list(self):                             # Test POST /operations/github/secrets/list
#         payload = dict(encrypted_pat = self.test_pat,
#                        target        = dict(owner = self.test_owner,
#                                             repo  = self.test_repo ))
#
#         response = self.client.post('/operations/github/secrets/list',
#                                     json=payload, headers=self.headers)
#
#         assert response.status_code == 200
#         data = response.json()
#         assert data['success']   is True
#         assert data['operation'] == 'github:secrets:list'
#         assert 'secrets'         in data['data']
#
#     # ═══════════════════════════════════════════════════════════════════════════════
#     # GitHub Secrets - Create Tests
#     # ═══════════════════════════════════════════════════════════════════════════════
#
#     def test__operations_github_secrets_create(self):                           # Test POST /operations/github/secrets/create
#         payload = dict(encrypted_pat   = self.test_pat                ,
#                        target          = dict(owner = self.test_owner ,
#                                               repo  = self.test_repo  ),
#                        secret_name     = 'TEST_SECRET'                ,
#                        encrypted_value = self.encrypted_value         )
#
#         response = self.client.post('/operations/github/secrets/create',
#                                     json=payload, headers=self.headers)
#
#         assert response.status_code == 200
#         data = response.json()
#         assert data['success']   is True
#         assert data['operation'] == 'github:secrets:create'
#
#         # Verify via surrogate state
#         state  = self.surrogate_context.surrogate.state
#         secret = state.get_repo_secret(self.test_owner, self.test_repo, 'TEST_SECRET')
#         assert secret is not None
#
#     # ═══════════════════════════════════════════════════════════════════════════════
#     # GitHub Secrets - Exists Tests
#     # ═══════════════════════════════════════════════════════════════════════════════
#
#     def test__operations_github_secrets_exists__true(self):                     # Test exists returns true for existing secret
#         # First create a secret
#         create_payload = dict(encrypted_pat   = self.test_pat                ,
#                               target          = dict(owner = self.test_owner ,
#                                                      repo  = self.test_repo  ),
#                               secret_name     = 'EXISTS_TEST'                ,
#                               encrypted_value = self.encrypted_value         )
#         self.client.post('/operations/github/secrets/create',
#                          json=create_payload, headers=self.headers)
#
#         # Then check exists
#         exists_payload = dict(encrypted_pat = self.test_pat                ,
#                               target        = dict(owner = self.test_owner ,
#                                                    repo  = self.test_repo  ),
#                               secret_name   = 'EXISTS_TEST'                )
#
#         response = self.client.post('/operations/github/secrets/exists',
#                                     json=exists_payload, headers=self.headers)
#
#         assert response.status_code == 200
#         data = response.json()
#         assert data['success']        is True
#         assert data['data']['exists'] is True
#
#     def test__operations_github_secrets_exists__false(self):                    # Test exists returns false for non-existent
#         payload = dict(encrypted_pat = self.test_pat                   ,
#                        target        = dict(owner = self.test_owner    ,
#                                             repo  = self.test_repo     ),
#                        secret_name   = 'NONEXISTENT_EXISTS_INTEGRATION')
#
#         response = self.client.post('/operations/github/secrets/exists',
#                                     json=payload, headers=self.headers)
#
#         assert response.status_code == 200
#         data = response.json()
#         assert data['success']        is True
#         assert data['data']['exists'] is False
#
#     # ═══════════════════════════════════════════════════════════════════════════════
#     # GitHub Secrets - Get Tests
#     # ═══════════════════════════════════════════════════════════════════════════════
#
#     def test__operations_github_secrets_get__exists(self):                      # Test get for existing secret
#         # First create a secret
#         create_payload = dict(encrypted_pat   = self.test_pat                ,
#                               target          = dict(owner = self.test_owner ,
#                                                      repo  = self.test_repo  ),
#                               secret_name     = 'GET_TEST'                   ,
#                               encrypted_value = self.encrypted_value         )
#         self.client.post('/operations/github/secrets/create',
#                          json=create_payload, headers=self.headers)
#
#         # Then get it
#         get_payload = dict(encrypted_pat = self.test_pat                ,
#                            target        = dict(owner = self.test_owner ,
#                                                 repo  = self.test_repo  ),
#                            secret_name   = 'GET_TEST'                   )
#
#         response = self.client.post('/operations/github/secrets/get',
#                                     json=get_payload, headers=self.headers)
#
#         assert response.status_code == 200
#         data = response.json()
#         assert data['success']   is True
#         assert data['operation'] == 'github:secrets:get'
#
#     def test__operations_github_secrets_get__not_exists(self):                  # Test get for non-existent secret
#         payload = dict(encrypted_pat = self.test_pat                ,
#                        target        = dict(owner = self.test_owner ,
#                                             repo  = self.test_repo  ),
#                        secret_name   = 'NONEXISTENT_GET_INTEGRATION')
#
#         response = self.client.post('/operations/github/secrets/get',
#                                     json=payload, headers=self.headers)
#
#         assert response.status_code == 200
#         data = response.json()
#         assert data['success'] is False
#
#     # ═══════════════════════════════════════════════════════════════════════════════
#     # GitHub Secrets - Delete Tests
#     # ═══════════════════════════════════════════════════════════════════════════════
#
#     def test__operations_github_secrets_delete(self):                           # Test delete
#         # First create a secret
#         create_payload = dict(encrypted_pat   = self.test_pat                ,
#                               target          = dict(owner = self.test_owner ,
#                                                      repo  = self.test_repo  ),
#                               secret_name     = 'TO_DELETE'                  ,
#                               encrypted_value = self.encrypted_value         )
#         self.client.post('/operations/github/secrets/create',
#                          json=create_payload, headers=self.headers)
#
#         # Then delete it
#         delete_payload = dict(encrypted_pat = self.test_pat                ,
#                               target        = dict(owner = self.test_owner ,
#                                                    repo  = self.test_repo  ),
#                               secret_name   = 'TO_DELETE'                  )
#
#         response = self.client.post('/operations/github/secrets/delete',
#                                     json=delete_payload, headers=self.headers)
#
#         assert response.status_code == 200
#         data = response.json()
#         assert data['success']   is True
#         assert data['operation'] == 'github:secrets:delete'
#
#         # Verify via surrogate state
#         state  = self.surrogate_context.surrogate.state
#         secret = state.get_repo_secret(self.test_owner, self.test_repo, 'TO_DELETE')
#         assert secret is None
#
#     # ═══════════════════════════════════════════════════════════════════════════════
#     # End-to-End Flow Tests
#     # ═══════════════════════════════════════════════════════════════════════════════
#
#     def test__flow__complete_crud(self):                                        # Test complete CRUD flow via HTTP client
#         target = dict(owner = self.test_owner, repo = self.test_repo)
#
#         # 1. Create multiple secrets
#         for name in ['FLOW_SECRET_1', 'FLOW_SECRET_2', 'FLOW_SECRET_3']:
#             create_response = self.client.post('/operations/github/secrets/create',
#                                                json=dict(encrypted_pat   = self.test_pat       ,
#                                                          target          = target              ,
#                                                          secret_name     = name                ,
#                                                          encrypted_value = self.encrypted_value),
#                                                headers=self.headers)
#             assert create_response.json()['success'] is True
#
#         # 2. List and verify secrets exist
#         list_response = self.client.post('/operations/github/secrets/list',
#                                          json=dict(encrypted_pat=self.test_pat, target=target),
#                                          headers=self.headers)
#         secret_names = [s['name'] for s in list_response.json()['data']['secrets']]
#         assert 'FLOW_SECRET_1' in secret_names
#         assert 'FLOW_SECRET_2' in secret_names
#         assert 'FLOW_SECRET_3' in secret_names
#
#         # 3. Check exists
#         exists_response = self.client.post('/operations/github/secrets/exists',
#                                            json=dict(encrypted_pat=self.test_pat, target=target, secret_name='FLOW_SECRET_2'),
#                                            headers=self.headers)
#         assert exists_response.json()['data']['exists'] is True
#
#         # 4. Delete one
#         delete_response = self.client.post('/operations/github/secrets/delete',
#                                            json=dict(encrypted_pat=self.test_pat, target=target, secret_name='FLOW_SECRET_2'),
#                                            headers=self.headers)
#         assert delete_response.json()['success'] is True
#
#         # 5. Verify deleted via list
#         list_response = self.client.post('/operations/github/secrets/list',
#                                          json=dict(encrypted_pat=self.test_pat, target=target),
#                                          headers=self.headers)
#         secret_names = [s['name'] for s in list_response.json()['data']['secrets']]
#         assert 'FLOW_SECRET_2' not in secret_names
#
#         # 6. Verify exists is now false
#         exists_response = self.client.post('/operations/github/secrets/exists',
#                                            json=dict(encrypted_pat=self.test_pat, target=target, secret_name='FLOW_SECRET_2'),
#                                            headers=self.headers)
#         assert exists_response.json()['data']['exists'] is False
#
#         # 7. Verify via surrogate state
#         state = self.surrogate_context.surrogate.state
#         secret_names = [s.name for s in state.list_repo_secrets(self.test_owner, self.test_repo)]
#         assert 'FLOW_SECRET_2' not in secret_names