import requests
import time
from typing                                                                             import Dict, Any, Optional
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url                import Safe_Str__Url
from mgraph_ai_service_deploy.config                                                    import GITHUB_SERVICE_URL
from mgraph_ai_service_deploy.schemas.common.Schema__Rate_Limit                         import Schema__Rate_Limit
from mgraph_ai_service_deploy.schemas.common.Schema__Response__Operation                import Schema__Response__Operation
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__List     import Schema__Request__GitHub__Secrets__List
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Get      import Schema__Request__GitHub__Secrets__Get
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Exists   import Schema__Request__GitHub__Secrets__Exists
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Create   import Schema__Request__GitHub__Secrets__Create
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Delete   import Schema__Request__GitHub__Secrets__Delete
from mgraph_ai_service_deploy.services.Auth__External_Services                          import Auth__External_Services


class Service__GitHub__Secrets(Type_Safe):
    github_service_url     : Safe_Str__Url = Safe_Str__Url(GITHUB_SERVICE_URL)  # GitHub Service base URL
    request_timeout        : int           = 30                                 # HTTP request timeout in seconds
    http_client            : Optional[Any] = None                               # Optional HTTP client (TestClient for tests)
    auth_external_services : Auth__External_Services                            # External service auth config

    def list_secrets(self, request: Schema__Request__GitHub__Secrets__List  # List all secrets in a repository
                     ) -> Schema__Response__Operation:
        start_time    = time.time()
        operation_id  = 'github:secrets:list'

        github_request = self.transform_list_request(request)
        result         = self.call_github_service('/github-secrets-repo/list', github_request)

        return self.build_response(result       = result       ,
                                   operation_id = operation_id ,
                                   start_time   = start_time   ,
                                   data_key     = 'secrets'    )

    def get_secret(self, request: Schema__Request__GitHub__Secrets__Get     # Get metadata for a single secret
                   ) -> Schema__Response__Operation:
        start_time    = time.time()
        operation_id  = 'github:secrets:get'

        github_request = self.transform_get_request(request)
        result         = self.call_github_service('/github-secrets-repo/get', github_request)

        return self.build_response(result       = result       ,
                                   operation_id = operation_id ,
                                   start_time   = start_time   ,
                                   data_key     = 'secret'     )

    def secret_exists(self, request: Schema__Request__GitHub__Secrets__Exists   # Check if a secret exists
                      ) -> Schema__Response__Operation:
        start_time    = time.time()
        operation_id  = 'github:secrets:exists'

        github_request = self.transform_exists_request(request)
        result         = self.call_github_service('/github-secrets-repo/get', github_request)

        return self.build_exists_response(result       = result       ,
                                          operation_id = operation_id ,
                                          start_time   = start_time   ,
                                          secret_name  = str(request.secret_name))

    def create_secret(self, request: Schema__Request__GitHub__Secrets__Create   # Create or update a secret
                      ) -> Schema__Response__Operation:
        start_time    = time.time()
        operation_id  = 'github:secrets:create'

        github_request = self.transform_create_request(request)
        result         = self.call_github_service('/github-secrets-repo/create', github_request)

        return self.build_response(result       = result       ,
                                   operation_id = operation_id ,
                                   start_time   = start_time   ,
                                   data_key     = 'created'    )

    def delete_secret(self, request: Schema__Request__GitHub__Secrets__Delete   # Delete a secret
                      ) -> Schema__Response__Operation:
        start_time    = time.time()
        operation_id  = 'github:secrets:delete'

        github_request = self.transform_delete_request(request)
        result         = self.call_github_service_delete('/github-secrets-repo/delete', github_request)

        return self.build_response(result       = result       ,
                                   operation_id = operation_id ,
                                   start_time   = start_time   ,
                                   data_key     = 'deleted'    )

    # ═══════════════════════════════════════════════════════════════════════════
    # Request Transform Methods - Convert Deploy Service format to GitHub Service format
    # ═══════════════════════════════════════════════════════════════════════════

    def transform_list_request(self, request: Schema__Request__GitHub__Secrets__List    # Transform list request
                               ) -> Dict[str, Any]:
        return dict(encrypted_pat = str(request.encrypted_pat)  ,
                    request_data  = dict(owner = str(request.target.owner),
                                         repo  = str(request.target.repo )))

    def transform_get_request(self, request: Schema__Request__GitHub__Secrets__Get      # Transform get request
                              ) -> Dict[str, Any]:
        return dict(encrypted_pat = str(request.encrypted_pat)  ,
                    request_data  = dict(owner       = str(request.target.owner),
                                         repo        = str(request.target.repo ),
                                         secret_name = str(request.secret_name )))

    def transform_exists_request(self, request: Schema__Request__GitHub__Secrets__Exists    # Transform exists request
                                 ) -> Dict[str, Any]:
        return dict(encrypted_pat = str(request.encrypted_pat)  ,
                    request_data  = dict(owner       = str(request.target.owner),
                                         repo        = str(request.target.repo ),
                                         secret_name = str(request.secret_name )))

    def transform_create_request(self, request: Schema__Request__GitHub__Secrets__Create    # Transform create request
                                 ) -> Dict[str, Any]:
        return dict(encrypted_pat = str(request.encrypted_pat)    ,
                    request_data  = dict(owner           = str(request.target.owner   ),        # todo: see if we can just use Type_Safe objects conversions here
                                         repo            = str(request.target.repo    ),
                                         secret_name     = str(request.secret_name    ),
                                         encrypted_value = str(request.encrypted_value)))

    def transform_delete_request(self, request: Schema__Request__GitHub__Secrets__Delete    # Transform delete request
                                 ) -> Dict[str, Any]:
        return dict(encrypted_pat = str(request.encrypted_pat)  ,
                    request_data  = dict(owner       = str(request.target.owner),
                                         repo        = str(request.target.repo ),
                                         secret_name = str(request.secret_name )))

    # ═══════════════════════════════════════════════════════════════════════════
    # HTTP Methods - Call GitHub Service
    # ═══════════════════════════════════════════════════════════════════════════

    def call_github_service(self,                                           # Make POST request to GitHub Service
                            endpoint: str ,                                 # todo: fix the type safety of these params
                            payload : Dict[str, Any]
                       ) -> Dict[str, Any]:
        if self.http_client:                                                # Use injected client (for tests)
            response = self.http_client.post(endpoint, json=payload)
        else:                                                               # Use requests (production)
            auth_config = self.auth_external_services.config__graph_service()
            if auth_config.enabled:
                target_server = auth_config.target_server
                headers       = {auth_config.key_name: auth_config.key_value}
                url           = f"{target_server}{endpoint}"
                response      = requests.post(url, json=payload, headers=headers, timeout=self.request_timeout)
            else:
                raise Exception("GitHub Service auth not configured")
        return response.json()

    def call_github_service_delete(self,                                    # Make DELETE request to GitHub Service
                                   endpoint: str,
                                   payload : Dict[str, Any]
                              ) -> Dict[str, Any]:
        if self.http_client:                                                # Use injected client (for tests)
            response = self.http_client.request("DELETE", endpoint, json=payload)
        else:                                                               # Use requests (production)
            auth_config = self.auth_external_services.config__graph_service()
            if auth_config.enabled:
                target_server = auth_config.target_server
                headers       = {auth_config.key_name: auth_config.key_value}
                url           = f"{target_server}{endpoint}"
                response      = requests.delete(url, json=payload, headers=headers, timeout=self.request_timeout)
            else:
                raise Exception("GitHub Service auth not configured")
        return response.json()

    # ═══════════════════════════════════════════════════════════════════════════
    # Response Builder Methods - Convert GitHub Service response to Deploy Service format
    # ═══════════════════════════════════════════════════════════════════════════

    def build_response(self, result      : Dict[str, Any] ,                 # Build standard operation response
                             operation_id: str            ,
                             start_time  : float          ,
                             data_key    : str
                       ) -> Schema__Response__Operation:
        duration         = time.time() - start_time
        response_context = result.get('response_context', {})
        response_data    = result.get('response_data'   , {})
        success          = response_context.get('success', False)

        rate_limit = self.extract_rate_limit(response_context)

        if success:
            data = {data_key: response_data.get(data_key, response_data)}
        else:
            data = None

        error = None
        if not success:
            errors = response_context.get('errors', [])
            error  = errors[0] if errors else response_context.get('message', 'Unknown error')

        return Schema__Response__Operation(success    = success      ,
                                           operation  = operation_id ,
                                           data       = data         ,
                                           error      = error        ,
                                           duration   = duration     ,
                                           rate_limit = rate_limit   )

    def build_exists_response(self, result      : Dict[str, Any] ,          # Build exists check response
                                    operation_id: str            ,
                                    start_time  : float          ,
                                    secret_name : str
                              ) -> Schema__Response__Operation:
        duration         = time.time() - start_time
        response_context = result.get('response_context', {})
        status_code      = response_context.get('status_code', 0)

        rate_limit = self.extract_rate_limit(response_context)

        exists = status_code == 200                                         # 200 means secret exists, 404 means it doesn't

        return Schema__Response__Operation(success    = True                                     ,
                                           operation  = operation_id                             ,
                                           data       = {'exists': exists, 'secret_name': secret_name},
                                           error      = None                                     ,
                                           duration   = duration                                 ,
                                           rate_limit = rate_limit                               )

    def extract_rate_limit(self, response_context: Dict[str, Any]           # Extract rate limit from response
                           ) -> Schema__Rate_Limit:
        rate_limit_data = response_context.get('rate_limit', {})
        return Schema__Rate_Limit(remaining           = rate_limit_data.get('remaining', 0),
                                  limit               = rate_limit_data.get('limit'    , 0),
                                  timestamp_reset     = rate_limit_data.get('reset'    , 0),
                                  used                = rate_limit_data.get('used'     , 0))
