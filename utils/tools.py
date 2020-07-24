import os
import re
import sys


def abspath(path: str) -> str:
    cwd = sys.argv[1]
    if path[0] == ".":
        return os.path.join(cwd, path[1:])
    if path[1] != ":":
        return os.path.join(cwd, path)
    return path


class ReSearching:
    param_search = re.compile("(\{\{ *([A-z0-9_]+){1} *('[A-z0-9._-]+'){1} *('[A-z0-9._-]+')* *\}\})")
    keywords_search = re.compile("(\{\{ *([A-z0-9_]+) *\}\})")
    path_search = re.compile("(:[A-z0-9_]+)")

    @classmethod
    def search_keywoards(cls, string: str) -> 'List[str]':
        return cls.keywords_search.findall(string)

    @classmethod
    def search_params(cls, string: str) -> 'List[str]':
        return cls.param_search.findall(string)

    @classmethod
    def search_path(cls, string: str) -> 'List[str]':
        return cls.path_search.findall(string)
