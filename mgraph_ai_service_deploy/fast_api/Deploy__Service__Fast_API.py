from osbot_fast_api.api.routes.Routes__Set_Cookie                               import Routes__Set_Cookie
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API                    import Serverless__Fast_API
from osbot_fast_api_serverless.fast_api.routes.Routes__Info                     import Routes__Info
from mgraph_ai_service_deploy.config                                            import FAST_API__TITLE, FAST_API__DESCRIPTION
from mgraph_ai_service_deploy.utils.Version                                     import version__mgraph_ai_service_deploy
from mgraph_ai_service_deploy.fast_api.routes.Routes__Public_Keys               import Routes__Public_Keys
from mgraph_ai_service_deploy.fast_api.routes.Routes__Operations__GitHub__Secrets import Routes__Operations__GitHub__Secrets


class Deploy__Service__Fast_API(Serverless__Fast_API):

    def setup(self):                                                                        # Configure FastAPI application settings
        with self.config as _:
            _.name   = FAST_API__TITLE
            _.version = version__mgraph_ai_service_deploy
        return super().setup()

    def setup_routes(self):
        self.add_routes(Routes__Public_Keys               )
        self.add_routes(Routes__Operations__GitHub__Secrets)
        self.add_routes(Routes__Info                      )
        self.add_routes(Routes__Set_Cookie                )
