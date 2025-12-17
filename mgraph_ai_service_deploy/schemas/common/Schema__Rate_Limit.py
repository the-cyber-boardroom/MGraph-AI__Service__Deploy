from osbot_utils.type_safe.Type_Safe                import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt


class Schema__Rate_Limit(Type_Safe):
    remaining           : Safe_UInt                                                # Remaining API calls
    limit               : Safe_UInt                                                # Total limit per hour
    timestamp_reset     : Safe_UInt                                                # Unix timestamp when limit resets
    used                : Safe_UInt                                                # Calls used in current window
