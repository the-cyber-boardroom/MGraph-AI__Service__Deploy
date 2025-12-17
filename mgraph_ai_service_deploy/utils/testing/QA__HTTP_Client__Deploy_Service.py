import pytest
from typing                                                                         import Dict
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url            import Safe_Str__Url
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.utils.Env                                                          import get_env, load_dotenv
from requests                                                                       import Session, Response

from mgraph_ai_service_deploy.config import ENV_VAR__DEPLOY_SERVICE__URL, ENV_VAR__GIT_HUB__ACCESS_TOKEN, ENV_VAR__DEPLOY_SERVICE__API_KEY__VALUE


class QA__HTTP_Client__Deploy_Service(Type_Safe):                                                   # HTTP client for QA tests against Deploy Service
    service_url    : Safe_Str__Url   = None
    api_key_name   : Safe_Str__Text  = None
    api_key_value  : Safe_Str__Text  = None
    session        : Session         = None
    timeout        : int             = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.session is None:
            self.session = Session()

    def auth_headers(self) -> Dict[str, str]:                                       # Headers with API key authentication
        if self.api_key_name and self.api_key_value:
            return {str(self.api_key_name): str(self.api_key_value)}
        return {}

    def url_for(self, path: str) -> str:                                            # Build full URL for endpoint
        return f"{self.service_url}{path}"

    def get(self, path: str, headers: dict = None) -> Response:                     # GET request with authentication
        request_headers = self.auth_headers()
        if headers:
            request_headers.update(headers)
        return self.session.get(url     = self.url_for(path) ,
                                headers = request_headers    ,
                                timeout = self.timeout       )

    def post(self, path: str, json: dict = None, headers: dict = None) -> Response: # POST request with authentication
        request_headers = self.auth_headers()
        if headers:
            request_headers.update(headers)
        return self.session.post(url     = self.url_for(path) ,
                                 json    = json               ,
                                 headers = request_headers    ,
                                 timeout = self.timeout       )

    def delete(self, path: str, json: dict = None, headers: dict = None) -> Response:   # DELETE request with authentication
        request_headers = self.auth_headers()
        if headers:
            request_headers.update(headers)
        return self.session.delete(url     = self.url_for(path) ,
                                   json    = json               ,
                                   headers = request_headers    ,
                                   timeout = self.timeout       )




