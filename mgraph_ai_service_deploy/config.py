SERVICE_NAME                         = 'mgraph_ai_service_deploy'
FAST_API__TITLE                      = "MGraph-AI Service Deploy"
FAST_API__DESCRIPTION                = "Infrastructure deployment orchestration service"

LAMBDA_DEPENDENCIES__DEPLOY__SERVICE = ['osbot-fast-api-serverless==v1.32.0']

GITHUB_SERVICE_URL                   = 'https://github.dev.mgraph.ai'


ENV_VAR__URL__TARGET_SERVER__GITHUB_SERVICE             = 'URL__TARGET_SERVER__GITHUB_SERVICE'
ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_NAME  = 'AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_NAME'
ENV_VAR__AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_VALUE = 'AUTH__TARGET_SERVER__GITHUB_SERVICE__KEY_VALUE'

ENV_VAR__DEPLOY_SERVICE__URL                            = 'DEPLOY_SERVICE__URL'
ENV_VAR__DEPLOY_SERVICE__API_KEY__NAME                  = 'DEPLOY_SERVICE__API_KEY__NAME'
ENV_VAR__DEPLOY_SERVICE__API_KEY__VALUE                 = 'DEPLOY_SERVICE__API_KEY__VALUE'
ENV_VAR__GIT_HUB__ACCESS_TOKEN                          = 'GIT_HUB__ACCESS_TOKEN'