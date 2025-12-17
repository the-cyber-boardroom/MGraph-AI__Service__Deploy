import base64
from typing                                                                         import Dict, Any, List
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url            import Safe_Str__Url
from osbot_utils.utils.Env                                                          import get_env
from mgraph_ai_service_deploy.config                                                import ENV_VAR__DEPLOY_SERVICE__URL, ENV_VAR__DEPLOY_SERVICE__API_KEY__NAME, ENV_VAR__DEPLOY_SERVICE__API_KEY__VALUE, ENV_VAR__GIT_HUB__ACCESS_TOKEN
from mgraph_ai_service_deploy.utils.testing.QA__HTTP_Client__Deploy_Service         import QA__HTTP_Client__Deploy_Service


class QA__Deploy_Service_Client(Type_Safe):                                         # High-level client for Deploy Service operations
    http_client        : QA__HTTP_Client__Deploy_Service = None
    github_pat         : str             = None                                     # Raw GitHub PAT (will be encrypted before use)
    cached_public_key  : str             = None                                     # Cached NaCl public key from service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Public Key Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def get_github_public_key(self) -> Dict[str, Any]:                              # GET /public-keys/github
        response = self.http_client.get('/public-keys/github')
        response.raise_for_status()
        return response.json()

    def public_key(self) -> str:                                                    # Get and cache the NaCl public key
        if self.cached_public_key is None:
            result = self.get_github_public_key()
            self.cached_public_key = result.get('public_key')
        return self.cached_public_key

    # ═══════════════════════════════════════════════════════════════════════════════
    # Encryption Helpers
    # ═══════════════════════════════════════════════════════════════════════════════

    def encrypt_value(self, value: str) -> str:                                     # Encrypt a value using NaCl SealedBox
        from nacl.public import SealedBox, PublicKey

        public_key_hex = self.public_key()
        pub_key_bytes  = bytes.fromhex(public_key_hex)
        nacl_pub_key   = PublicKey(pub_key_bytes)
        sealed_box     = SealedBox(nacl_pub_key)
        encrypted      = sealed_box.encrypt(value.encode())
        return base64.b64encode(encrypted).decode()

    def encrypted_pat(self) -> str:                                                 # Get encrypted version of the GitHub PAT
        if not self.github_pat:
            raise ValueError("GitHub PAT not configured")
        return self.encrypt_value(self.github_pat)

    # ═══════════════════════════════════════════════════════════════════════════════
    # GitHub Secrets Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def secrets_list(self, owner: str, repo: str) -> Dict[str, Any]:                # POST /operations/github/secrets/list
        payload = dict(encrypted_pat = self.encrypted_pat()        ,
                       target        = dict(owner = owner          ,
                                            repo  = repo           ))
        response = self.http_client.post('/operations/github/secrets/list', json=payload)
        response.raise_for_status()
        return response.json()

    def secrets_get(self, owner: str, repo: str, secret_name: str) -> Dict[str, Any]:   # POST /operations/github/secrets/get
        payload = dict(encrypted_pat = self.encrypted_pat()        ,
                       target        = dict(owner = owner          ,
                                            repo  = repo           ),
                       secret_name   = secret_name                 )
        response = self.http_client.post('/operations/github/secrets/get', json=payload)
        response.raise_for_status()
        return response.json()

    def secrets_exists(self, owner: str, repo: str, secret_name: str) -> Dict[str, Any]:    # POST /operations/github/secrets/exists
        payload = dict(encrypted_pat = self.encrypted_pat()        ,
                       target        = dict(owner = owner          ,
                                            repo  = repo           ),
                       secret_name   = secret_name                 )
        response = self.http_client.post('/operations/github/secrets/exists', json=payload)
        response.raise_for_status()
        return response.json()

    def secrets_create(self, owner: str, repo: str,                                 # POST /operations/github/secrets/create
                       secret_name: str, secret_value: str
                       ) -> Dict[str, Any]:
        encrypted_value = self.encrypt_value(secret_value)
        payload = dict(encrypted_pat   = self.encrypted_pat()      ,
                       target          = dict(owner = owner        ,
                                              repo  = repo         ),
                       secret_name     = secret_name               ,
                       encrypted_value = encrypted_value           )
        response = self.http_client.post('/operations/github/secrets/create', json=payload)
        response.raise_for_status()
        return response.json()

    def secrets_delete(self, owner: str, repo: str, secret_name: str) -> Dict[str, Any]:    # POST /operations/github/secrets/delete
        payload = dict(encrypted_pat = self.encrypted_pat()        ,
                       target        = dict(owner = owner          ,
                                            repo  = repo           ),
                       secret_name   = secret_name                 )
        response = self.http_client.post('/operations/github/secrets/delete', json=payload)
        response.raise_for_status()
        return response.json()

    # ═══════════════════════════════════════════════════════════════════════════════
    # Convenience Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def secret_exists(self, owner: str, repo: str, secret_name: str) -> bool:       # Check if secret exists (returns bool)
        result = self.secrets_exists(owner, repo, secret_name)
        return result.get('data', {}).get('exists', False)

    def list_secret_names(self, owner: str, repo: str) -> List[str]:                # List secret names (returns list of strings)
        result = self.secrets_list(owner, repo)
        secrets = result.get('data', {}).get('secrets', [])
        return [s.get('name') for s in secrets]

    def set_secret(self, owner: str, repo: str,                                     # Create/update secret (alias for secrets_create)
                   secret_name: str, secret_value: str
                   ) -> bool:
        result = self.secrets_create(owner, repo, secret_name, secret_value)
        return result.get('success', False)

    def set_secrets(self, owner: str, repo: str,                                    # Bulk set multiple secrets
                    secrets: Dict[str, str]
                    ) -> Dict[str, bool]:
        results = {}
        for name, value in secrets.items():
            results[name] = self.set_secret(owner, repo, name, value)
        return results

def create_deploy_client(service_url  : str = None,                                 # Factory function to create a Deploy Service client
                         api_key_name : str = None,
                         api_key_value: str = None,
                         github_pat   : str = None
                         ) -> QA__Deploy_Service_Client:

    service_url   = service_url   or get_env(ENV_VAR__DEPLOY_SERVICE__URL           )
    api_key_name  = api_key_name  or get_env(ENV_VAR__DEPLOY_SERVICE__API_KEY__NAME )
    api_key_value = api_key_value or get_env(ENV_VAR__DEPLOY_SERVICE__API_KEY__VALUE)
    github_pat    = github_pat    or get_env(ENV_VAR__GIT_HUB__ACCESS_TOKEN         )

    if service_url and api_key_name and api_key_value and github_pat:
        http_client = QA__HTTP_Client__Deploy_Service(service_url   = Safe_Str__Url (service_url),
                                                      api_key_name  = Safe_Str__Text(api_key_name ) if api_key_name  else None,
                                                      api_key_value = Safe_Str__Text(api_key_value) if api_key_value else None)
    else:
        raise Exception('service_url and api_key_name are required')

    return QA__Deploy_Service_Client(
        http_client = http_client ,
        github_pat  = github_pat  )