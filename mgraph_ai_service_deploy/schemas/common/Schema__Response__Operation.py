from typing                                                                    import Optional, Any, Dict

from mgraph_ai_service_github.schemas.safe_str.Safe_Str__Error_Message import Safe_Str__Text_Message
from osbot_utils.type_safe.Type_Safe                                           import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from osbot_utils.type_safe.primitives.core.Safe_Float                          import Safe_Float
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label import Safe_Str__Label

from mgraph_ai_service_deploy.schemas.common.Schema__Rate_Limit                import Schema__Rate_Limit


class Schema__Response__Operation(Type_Safe):
    success    : bool                                                       # Whether operation succeeded
    operation  : Safe_Str__Label                                            # Operation identifier (e.g., github:secrets:list)
    data       : Dict[str, Any]                                             # Operation-specific response data
    error      : Safe_Str__Text_Message                                     # Error message if failed
    duration   : Safe_Float                                                 # Operation duration in seconds
    rate_limit : Schema__Rate_Limit                                         # GitHub API rate limit info
