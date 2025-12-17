from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str
import re


class Safe_Str__Encrypted__Base64(Safe_Str):
    regex        = re.compile(r'[^A-Za-z0-9+/=]')                           # Base64 characters only
    max_length   = 65536                                                    # Allow large encrypted blobs
    min_length   = 10                                                       # Encrypted data has minimum size
    #allow_empty  = False                                                    # Must have content | todo: see side effect of this on OSBot-Utils
