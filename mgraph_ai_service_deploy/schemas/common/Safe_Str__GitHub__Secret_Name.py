from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str
import re


class Safe_Str__GitHub__Secret_Name(Safe_Str):
    regex        = re.compile(r'[^A-Za-z0-9_]')                             # Alphanumerics and underscores only
    max_length   = 255                                                      # GitHub maximum
    min_length   = 1                                                        # Must have content
    #allow_empty  = False                                                    # Cannot be empty

    def __new__(cls, value=''):
        if value:
            if value[0].isdigit():                                          # Cannot start with number
                raise ValueError(f"Secret name cannot start with a number: {value}")
            if value.startswith('GITHUB_'):                                 # Reserved prefix
                raise ValueError(f"Secret name cannot start with 'GITHUB_': {value}")
        return super().__new__(cls, value)
