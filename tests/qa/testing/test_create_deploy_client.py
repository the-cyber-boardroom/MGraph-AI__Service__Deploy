from unittest                                                               import TestCase
from mgraph_ai_service_deploy.utils.testing.QA__Deploy_Service_Client       import QA__Deploy_Service_Client, create_deploy_client
from mgraph_ai_service_deploy.utils.testing.QA__HTTP_Client__Deploy_Service import QA__HTTP_Client__Deploy_Service
from mgraph_ai_service_deploy.utils.testing.QA__Test_Objs                   import skip_if_no_api_key, skip_if_no_github_pat


class test_create_deploy_client(TestCase):

    def test_factory_function(self):
        skip_if_no_api_key()
        skip_if_no_github_pat()

        client = create_deploy_client()

        assert type(client)             is QA__Deploy_Service_Client
        assert type(client.http_client) is QA__HTTP_Client__Deploy_Service

    def test_factory_with_explicit_params(self):
        client = create_deploy_client(service_url   = 'http://localhost:8080',
                                      api_key_name  = 'x-custom-key',
                                      api_key_value = 'test-key',
                                      github_pat    = 'ghp_test')

        assert str(client.http_client.service_url)   == 'http://localhost:8080'
        assert str(client.http_client.api_key_name)  == 'x-custom-key'
        assert str(client.http_client.api_key_value) == 'test-key'
        assert client.github_pat                     == 'ghp_test'