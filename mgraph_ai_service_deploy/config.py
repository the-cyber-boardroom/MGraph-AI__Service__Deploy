from mgraph_ai_service_deploy import package_name

SERVICE_NAME                         = package_name
FAST_API__TITLE                      = "MGraph-AI Service Deploy"
FAST_API__DESCRIPTION                = "Infrastructure deployment orchestration service"

LAMBDA_DEPENDENCIES__DEPLOY__SERVICE = ['osbot-fast-api-serverless==v1.32.0',
                                        ]

GITHUB_SERVICE_URL                   = 'https://github.dev.mgraph.ai'
