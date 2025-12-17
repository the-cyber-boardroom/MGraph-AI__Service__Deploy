import pytest
from unittest                                                               import TestCase
from osbot_utils.utils.Env                                                  import load_dotenv
from osbot_utils.utils.Files                                                import path_combine, file_not_exists
from mgraph_ai_service_deploy.utils.testing.QA__Deploy_Service_Client       import QA__Deploy_Service_Client, create_deploy_client
from mgraph_ai_service_deploy.utils.testing.QA__HTTP_Client__Deploy_Service import QA__HTTP_Client__Deploy_Service
from mgraph_ai_service_deploy.utils.testing.QA__Test_Objs                   import setup__qa_test_objs, skip_if_no_api_key, skip_if_no_github_pat
from tests                                                                  import qa

QA__GITHUB__REPO__OWNER = 'the-cyber-boardroom'
QA__GITHUB__REPO__NAME = 'MGraph-AI__Service__Deploy'

class test_QA__HTTP_Client__Deploy_Service(TestCase):

    @classmethod
    def setUpClass(cls):
        env_file_name = '.qa.env'
        env_file      = path_combine(qa.path,env_file_name)
        if file_not_exists(env_file):
            pytest.skip(f"could not find env file {env_file_name} in the qa folder")
        load_dotenv(dotenv_path=env_file, override=True)
        skip_if_no_api_key()
        skip_if_no_github_pat()
        cls.qa_objs = setup__qa_test_objs()
        cls.client  = cls.qa_objs.deploy_client
        cls.owner   = QA__GITHUB__REPO__OWNER
        cls.repo    = QA__GITHUB__REPO__NAME

    # ═══════════════════════════════════════════════════════════════════════════════
    # Setup Verification
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_setUpClass(self):
        assert type(self.client)             is QA__Deploy_Service_Client
        assert type(self.client.http_client) is QA__HTTP_Client__Deploy_Service
        assert self.client.github_pat        is not None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Public Key Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get_github_public_key(self):
        result = self.client.get_github_public_key()

        assert 'public_key' in result
        assert 'algorithm'  in result
        assert 'service'    in result
        assert result['service']   == 'github'
        assert result['algorithm'] == 'NaCl/Curve25519/SealedBox'
        assert len(result['public_key']) == 64                                  # 32 bytes hex encoded

    def test_public_key_cached(self):
        key1 = self.client.public_key()
        key2 = self.client.public_key()

        assert key1 == key2
        assert self.client.cached_public_key == key1

    # ═══════════════════════════════════════════════════════════════════════════════
    # Encryption Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_encrypt_value(self):
        encrypted = self.client.encrypt_value('test-secret-value')

        assert type(encrypted) is str
        import base64
        decoded = base64.b64decode(encrypted)
        assert len(decoded) >= 48                                               # NaCl SealedBox minimum size

    def test_encrypted_pat(self):
        encrypted = self.client.encrypted_pat()

        assert type(encrypted) is str
        import base64
        decoded = base64.b64decode(encrypted)
        assert len(decoded) >= 48

    # ═══════════════════════════════════════════════════════════════════════════════
    # Secrets List Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_secrets_list(self):
        result = self.client.secrets_list(self.owner, self.repo)

        assert result.get('success')   is True
        assert result.get('operation') == 'github:secrets:list'
        assert 'data'                  in result
        assert 'secrets'               in result['data']

    def test_list_secret_names(self):
        names = self.client.list_secret_names(self.owner, self.repo)

        assert type(names) is list
        # All names should be strings
        for name in names:
            assert type(name) is str

    # ═══════════════════════════════════════════════════════════════════════════════
    # Secrets Exists Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_secrets_exists__true(self):
        # First check what secrets exist
        names = self.client.list_secret_names(self.owner, self.repo)
        if names:
            result = self.client.secrets_exists(self.owner, self.repo, names[0])

            assert result.get('success')        is True
            assert result.get('operation')      == 'github:secrets:exists'
            assert result['data'].get('exists') is True

    def test_secrets_exists__false(self):
        result = self.client.secrets_exists(self.owner, self.repo, 'NONEXISTENT_SECRET_12345')

        assert result.get('success')        is True
        assert result['data'].get('exists') is False

    def test_secret_exists_convenience(self):
        exists = self.client.secret_exists(self.owner, self.repo, 'NONEXISTENT_SECRET_12345')

        assert exists is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Secrets CRUD Tests (be careful - these modify real secrets!)
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_secrets_crud_flow(self):
        secret_name  = 'QA_TEST_SECRET__DELETE_ME'
        secret_value = 'test-value-12345'

        # Create
        create_result = self.client.secrets_create(
            self.owner, self.repo, secret_name, secret_value)
        assert create_result.get('success') is True

        # Exists
        assert self.client.secret_exists(self.owner, self.repo, secret_name) is True

        # Get
        get_result = self.client.secrets_get(self.owner, self.repo, secret_name)
        assert get_result.get('success') is True
        assert get_result['data']['secret']['name'] == secret_name

        # Delete
        delete_result = self.client.secrets_delete(self.owner, self.repo, secret_name)
        assert delete_result.get('success') is True

        # Verify deleted
        assert self.client.secret_exists(self.owner, self.repo, secret_name) is False



