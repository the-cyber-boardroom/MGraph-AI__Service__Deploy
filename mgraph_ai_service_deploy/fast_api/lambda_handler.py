import os

if os.getenv('AWS_REGION'):                                                     # Only execute if running inside AWS Lambda

    from osbot_aws.aws.lambda_.boto3__lambda import load_dependencies           # Lightweight boto3 loader
    from mgraph_ai_service_deploy.config     import LAMBDA_DEPENDENCIES__DEPLOY__SERVICE

    load_dependencies(LAMBDA_DEPENDENCIES__DEPLOY__SERVICE)

    def clear_osbot_modules():                                                  # Clean up after dependency loading
        import sys
        for module in list(sys.modules):
            if module.startswith('osbot_aws'):
                del sys.modules[module]

    clear_osbot_modules()

error   = None                                                                  # Pin these variables
handler = None
app     = None

try:
    from mgraph_ai_service_deploy.fast_api.Deploy__Service__Fast_API import Deploy__Service__Fast_API
    with Deploy__Service__Fast_API() as _:
        _.setup()
        handler = _.handler()
        app     = _.app()
except Exception as exc:
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME") is None:                           # Raise exception when not in Lambda
        raise
    error = (f"CRITICAL ERROR: Failed to start service with:\n\n"
             f"{type(exc).__name__}: {exc}")


def run(event, context=None):
    if error:
        return error
    return handler(event, context)
