import pytest
from unittest                                                   import TestCase
from osbot_utils.utils.Dev                                      import pprint
from osbot_utils.utils.Env                                      import load_dotenv, get_env
from osbot_utils.utils.Files                                    import path_combine, file_not_exists
from mgraph_ai_service_deploy.utils.testing.QA__Test_Objs       import skip_if_no_api_key, skip_if_no_github_pat, setup__qa_test_objs
from tests                                                      import qa

ENV_VAR__SETUP__TARGET__GITHUB__REPO__OWNER = 'SETUP__TARGET__GITHUB__REPO__OWNER'
ENV_VAR__SETUP__TARGET__GITHUB__REPO__NAME  = 'SETUP__TARGET__GITHUB__REPO__NAME'
ENV_VAR__SETUP__TARGET__ENV_VARS_TO_SET     = 'SETUP__TARGET__ENV_VARS_TO_SET'


class test__configure__deploy_service(TestCase):

    @classmethod
    def setUpClass(cls):
        env_file_name = '.qa.env'
        env_file      = path_combine(qa.path,env_file_name)
        if file_not_exists(env_file):
            pytest.skip(f"could not find env file {env_file_name} in the qa folder")
        load_dotenv(dotenv_path=env_file, override=True)
        skip_if_no_api_key()
        skip_if_no_github_pat()
        cls.qa_objs      = setup__qa_test_objs()
        cls.client       = cls.qa_objs.deploy_client


    def test__configure_via_service(self):
        repo_owner      = get_env(ENV_VAR__SETUP__TARGET__GITHUB__REPO__OWNER)
        repo_name       = get_env(ENV_VAR__SETUP__TARGET__GITHUB__REPO__NAME )
        env_vars_to_set = get_env(ENV_VAR__SETUP__TARGET__ENV_VARS_TO_SET).split(',')
        print()
        print("\n🚀 Starting service configuration")
        print(f"📦 Repository: {repo_owner}/{repo_name}")
        print("─" * 40)

        with self.client as _:
            for env_var in env_vars_to_set:
                env_var = env_var.strip()
                env_value = get_env(env_var)

                if not env_value:
                    print(f"  ❌ Missing value for env var: {env_var}")
                else:
                    print(f"  🔧 Configuring env var: {env_var}")

                    exists = _.secret_exists(owner       = repo_owner,
                                             repo        = repo_name ,
                                             secret_name = env_var   )
                    if exists:
                        print("    ✅ Secret already exists — nothing to do")
                    else:
                        print("    🆕 Secret does not exist — creating it")

                        result = _.secrets_create(owner        = repo_owner,
                                                  repo         = repo_name ,
                                                  secret_name  = env_var   ,
                                                  secret_value = env_value )

                        if result.get("success") is True:
                            print("    📤 Secret created successfully")
                        else:
                            print("    ❌ Secret creation failed")
                            print("    📄 Response:")
                            pprint(result)

        print("─" * 40)
        print("✅ Configuration complete\n")




