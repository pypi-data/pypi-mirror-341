import pytest

from keylex.matchers.keyword import Keyword
from keylex.matchers.keyword_list import KeywordList

@pytest.fixture
def empty_keyword():
    """Returns a new empty Keyword instance."""
    return Keyword("test")

@pytest.fixture
def filled_keyword():
    """Returns a Keyword with synonyms and acronyms."""
    kw = Keyword("python")
    kw.add_synonyms(["snake", "anaconda"])
    kw.add_acronyms(["PY", "PYT"])
    return kw

@pytest.fixture
def empty_keyword_list():
    """Returns an empty KeywordList."""
    return KeywordList()

@pytest.fixture
def filled_keyword_list():
    """Returns a KeywordList with several keywords."""
    kw1 = Keyword("python")
    kw1.add_synonyms(["snake", "anaconda"])
    kw1.add_acronyms(["PY"])
    
    kw2 = Keyword("javascript")
    kw2.add_synonyms(["js", "ecmascript"])
    kw2.add_acronyms(["JS"])
    
    return KeywordList([kw1, kw2])

@pytest.fixture
def programming_dict():
    """Returns a dictionary for creating a KeywordList."""
    return {
        "Python": ["py", "python3", {"acronyms": ["PY"]}],
        "JavaScript": ["js", "ecmascript", {"acronyms": ["JS"]}],
        "C++": ["cpp", {"synonyms": ["cplusplus", "c plus plus"]}]
    }