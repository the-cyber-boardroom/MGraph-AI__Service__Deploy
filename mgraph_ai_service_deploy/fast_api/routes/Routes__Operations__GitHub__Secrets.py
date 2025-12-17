from osbot_fast_api.api.routes.Fast_API__Routes                                     import Fast_API__Routes
from mgraph_ai_service_deploy.services.Service__GitHub__Secrets                     import Service__GitHub__Secrets
from mgraph_ai_service_deploy.schemas.common.Schema__Response__Operation            import Schema__Response__Operation
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__List   import Schema__Request__GitHub__Secrets__List
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Get    import Schema__Request__GitHub__Secrets__Get
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Exists import Schema__Request__GitHub__Secrets__Exists
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Create import Schema__Request__GitHub__Secrets__Create
from mgraph_ai_service_deploy.schemas.github.Schema__Request__GitHub__Secrets__Delete import Schema__Request__GitHub__Secrets__Delete


TAG__ROUTES_OPERATIONS_GITHUB_SECRETS = 'operations/github/secrets'

ROUTES_PATHS__OPERATIONS_GITHUB_SECRETS = [
    f'/{TAG__ROUTES_OPERATIONS_GITHUB_SECRETS}/list'   ,
    f'/{TAG__ROUTES_OPERATIONS_GITHUB_SECRETS}/get'    ,
    f'/{TAG__ROUTES_OPERATIONS_GITHUB_SECRETS}/exists' ,
    f'/{TAG__ROUTES_OPERATIONS_GITHUB_SECRETS}/create' ,
    f'/{TAG__ROUTES_OPERATIONS_GITHUB_SECRETS}/delete' ,
]


class Routes__Operations__GitHub__Secrets(Fast_API__Routes):
    tag : str = TAG__ROUTES_OPERATIONS_GITHUB_SECRETS                       # URL prefix: /operations/github/secrets

    service_github_secrets : Service__GitHub__Secrets                       # Injected by Type_Safe

    def list(self, request: Schema__Request__GitHub__Secrets__List          # POST /operations/github/secrets/list
             ) -> Schema__Response__Operation:
        return self.service_github_secrets.list_secrets(request)

    def get(self, request: Schema__Request__GitHub__Secrets__Get            # POST /operations/github/secrets/get
            ) -> Schema__Response__Operation:
        return self.service_github_secrets.get_secret(request)

    def exists(self, request: Schema__Request__GitHub__Secrets__Exists      # POST /operations/github/secrets/exists
               ) -> Schema__Response__Operation:
        return self.service_github_secrets.secret_exists(request)

    def create(self, request: Schema__Request__GitHub__Secrets__Create      # POST /operations/github/secrets/create
               ) -> Schema__Response__Operation:
        return self.service_github_secrets.create_secret(request)

    def delete(self, request: Schema__Request__GitHub__Secrets__Delete      # POST /operations/github/secrets/delete
               ) -> Schema__Response__Operation:
        return self.service_github_secrets.delete_secret(request)

    def setup_routes(self):                                                 # Register all routes
        self.add_route_post(self.list  )
        self.add_route_post(self.get   )
        self.add_route_post(self.exists)
        self.add_route_post(self.create)
        self.add_route_post(self.delete)
        return self
