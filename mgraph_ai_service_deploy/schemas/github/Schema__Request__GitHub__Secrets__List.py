from osbot_utils.type_safe.Type_Safe                                       import Type_Safe
from mgraph_ai_service_deploy.schemas.common.Safe_Str__Encrypted__Base64   import Safe_Str__Encrypted__Base64
from mgraph_ai_service_deploy.schemas.common.Schema__Target__GitHub__Repo  import Schema__Target__GitHub__Repo


class Schema__Request__GitHub__Secrets__List(Type_Safe):
    encrypted_pat : Safe_Str__Encrypted__Base64                             # Client-encrypted GitHub PAT
    target        : Schema__Target__GitHub__Repo                            # Target repository
