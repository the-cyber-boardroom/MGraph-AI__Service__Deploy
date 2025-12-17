from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Header__Name    import Safe_Str__Http__Header__Name
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Header__Value   import Safe_Str__Http__Header__Value
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url                    import Safe_Str__Url

class Schema__Auth__Config__External_Service(Type_Safe):
    target_server  : Safe_Str__Url                 = None
    key_name       : Safe_Str__Http__Header__Value = None                                       # Optional API key
    key_value      : Safe_Str__Http__Header__Name  = None                                       # Header name for API key
    enabled        : bool                          = False
