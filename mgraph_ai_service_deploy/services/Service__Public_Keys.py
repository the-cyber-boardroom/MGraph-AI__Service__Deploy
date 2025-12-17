from typing                                                                      import Dict, Any, Optional
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url         import Safe_Str__Url
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key import Safe_Str__Key
import requests

from mgraph_ai_service_deploy.config import GITHUB_SERVICE_URL
from mgraph_ai_service_deploy.services.Auth__External_Services import Auth__External_Services


class Service__Public_Keys(Type_Safe):
    #github_service_url     : Safe_Str__Url = Safe_Str__Url(GITHUB_SERVICE_URL)  # GitHub Service base URL
    request_timeout        : int           = 30                                 # HTTP request timeout in seconds
    http_client            : Optional[Any] = None                               # Optional HTTP client (TestClient for tests)
    auth_external_services : Auth__External_Services

    def get_github_public_key(self) -> Dict[str, Any]:                      # Fetch GitHub Service's NaCl public key
        endpoint = "/encryption/public-key"

        if self.http_client:                                                # Use injected client (for tests)
            response = self.http_client.get(endpoint)
        else:                                                               # Use requests (production)
            auth_config = self.auth_external_services.config__graph_service()
            if auth_config.enabled:
                target_server = auth_config.target_server
                headers       = {auth_config.key_name: auth_config.key_value}
                url           = f"{target_server}{endpoint}"
                response = requests.get(url, timeout=self.request_timeout, headers=headers)
                response.raise_for_status()
            else:
                raise Exception("GitHub Service auth not configured")

        data = response.json()
        return dict(public_key = data.get('public_key') ,
                    algorithm  = data.get('algorithm')  ,
                    service    = 'github'               )

    def get_public_key_for_service(self, service: Safe_Str__Key             # Get public key for named service
                                   ) -> Dict[str, Any]:
        if service == 'github':
            return self.get_github_public_key()
        raise ValueError(f"Unknown service: {service}")
