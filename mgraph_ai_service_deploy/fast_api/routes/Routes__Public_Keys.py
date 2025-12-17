from typing                                                   import Dict, Any
from osbot_fast_api.api.routes.Fast_API__Routes               import Fast_API__Routes
from mgraph_ai_service_deploy.services.Service__Public_Keys   import Service__Public_Keys


TAG__ROUTES_PUBLIC_KEYS = 'public-keys'

ROUTES_PATHS__PUBLIC_KEYS = [f'/{TAG__ROUTES_PUBLIC_KEYS}/github']


class Routes__Public_Keys(Fast_API__Routes):
    tag : str = TAG__ROUTES_PUBLIC_KEYS                                     # URL prefix: /public-keys

    service_public_keys : Service__Public_Keys                              # Injected by Type_Safe

    def github(self) -> Dict[str, Any]:                                     # GET /public-keys/github
        return self.service_public_keys.get_github_public_key()

    def setup_routes(self):                                                 # Register all routes
        self.add_route_get(self.github)
        return self
