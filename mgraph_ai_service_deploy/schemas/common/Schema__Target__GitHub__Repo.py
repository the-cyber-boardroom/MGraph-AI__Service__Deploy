from osbot_utils.type_safe.Type_Safe                                                         import Type_Safe
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner import Safe_Str__GitHub__Repo_Owner
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name  import Safe_Str__GitHub__Repo_Name


class Schema__Target__GitHub__Repo(Type_Safe):
    owner : Safe_Str__GitHub__Repo_Owner                                    # GitHub organization or username
    repo  : Safe_Str__GitHub__Repo_Name                                     # Repository name
