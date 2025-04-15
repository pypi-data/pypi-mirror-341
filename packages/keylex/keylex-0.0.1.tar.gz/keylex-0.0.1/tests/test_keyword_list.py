from keylex.matchers.keyword_list import KeywordList
from keylex.matchers.keyword import Keyword
import pytest
from .test_base import *

class TestKeywordList:
    """Tests for the KeywordList class."""
    
    def test_initialization(self):
        """Test basic initialization of KeywordList objects."""
        # Empty initialization
        kw_list = KeywordList()
        assert len(kw_list) == 0
        
        # Initialize with keywords
        kw1 = Keyword("test1")
        kw2 = Keyword("test2")
        kw_list2 = KeywordList([kw1, kw2])
        assert len(kw_list2) == 2
        assert "test1" in kw_list2.get_all_keywords()
        assert "test2" in kw_list2.get_all_keywords()
    
    def test_from_list(self):
        """Test creating KeywordList from a list of strings and Keyword objects."""
        kw = Keyword("existing")
        kw.add_synonyms(["old"])
        
        kw_list = KeywordList.from_list(["new1", "new2", kw])
        assert len(kw_list) == 3
        assert "new1" in kw_list.get_all_keywords()
        assert "new2" in kw_list.get_all_keywords()
        assert "existing" in kw_list.get_all_keywords()
        
        # Test with invalid type
        with pytest.raises(TypeError):
            KeywordList.from_list(["valid", 123])
    
    def test_from_dict(self, programming_dict):
        """Test creating KeywordList from a dictionary."""
        kw_list = KeywordList.from_dict(programming_dict)
        
        assert len(kw_list) == 3
        assert "Python" in kw_list.get_all_keywords()
        assert "JavaScript" in kw_list.get_all_keywords()
        assert "C++" in kw_list.get_all_keywords()
        
        # Check related terms were added correctly
        python_kw = kw_list.find_keyword("Python")
        assert "py" in python_kw.synonyms
        assert "python3" in python_kw.synonyms
        assert "PY" in python_kw.acronyms
        
        cpp_kw = kw_list.find_keyword("C++")
        assert "cplusplus" in cpp_kw.synonyms
        assert "c plus plus" in cpp_kw.synonyms
        
        # Test with invalid structure
        invalid_dict = {"invalid": [{"unknown_type": ["term"]}]}
        with pytest.raises(ValueError):
            KeywordList.from_dict(invalid_dict)
        
        invalid_type_dict = {"invalid": [123]}
        with pytest.raises(TypeError):
            KeywordList.from_dict(invalid_type_dict)
    
    def test_add_keyword(self, empty_keyword_list):
        """Test adding keywords to the list."""
        kw1 = Keyword("add1")
        kw2 = Keyword("add2")
        
        empty_keyword_list.add_keyword(kw1)
        assert len(empty_keyword_list) == 1
        assert "add1" in empty_keyword_list.get_all_keywords()
        
        empty_keyword_list.add_keyword(kw2)
        assert len(empty_keyword_list) == 2
        assert "add2" in empty_keyword_list.get_all_keywords()
        
        # Test duplicate prevention
        kw1_dup = Keyword("add1")
        empty_keyword_list.add_keyword(kw1_dup)
        assert len(empty_keyword_list) == 2  # Should not add duplicate
    
    def test_remove_keyword(self, filled_keyword_list):
        """Test removing keywords from the list."""
        kw_to_remove = filled_keyword_list.find_keyword("python")
        filled_keyword_list.remove_keyword(kw_to_remove)
        
        assert len(filled_keyword_list) == 1
        assert "python" not in filled_keyword_list.get_all_keywords()
        assert "javascript" in filled_keyword_list.get_all_keywords()
        
        # Test removing non-existent keyword
        nonexistent = Keyword("nonexistent")
        filled_keyword_list.remove_keyword(nonexistent)  # Should not error
        assert len(filled_keyword_list) == 1
    
    def test_clear(self, filled_keyword_list):
        """Test clearing all keywords from the list."""
        assert len(filled_keyword_list) > 0
        filled_keyword_list.clear()
        assert len(filled_keyword_list) == 0
        assert len(filled_keyword_list.get_all_keywords()) == 0
    
    def test_get_all_keywords(self, filled_keyword_list):
        """Test getting all primary keywords."""
        keywords = filled_keyword_list.get_all_keywords()
        assert len(keywords) == 2
        assert "python" in keywords
        assert "javascript" in keywords
    
    def test_get_all_related_terms(self, filled_keyword_list):
        """Test getting all related terms."""
        related_terms_list = filled_keyword_list.get_all_related_terms()
        assert len(related_terms_list) == 2
        
        # Check first keyword terms
        assert "python" in related_terms_list[0]
        assert "snake" in related_terms_list[0]
        assert "anaconda" in related_terms_list[0]
        assert "PY" in related_terms_list[0]
        
        # Check second keyword terms
        assert "javascript" in related_terms_list[1]
        assert "js" in related_terms_list[1]
        assert "ecmascript" in related_terms_list[1]
        assert "JS" in related_terms_list[1]
    
    def test_find_keyword(self, filled_keyword_list):
        """Test finding a keyword by term."""
        # Find by primary keyword
        found1 = filled_keyword_list.find_keyword("python")
        assert found1 is not None
        assert found1.keyword == "python"
        
        # Find by synonym
        found2 = filled_keyword_list.find_keyword("snake")
        assert found2 is not None
        assert found2.keyword == "python"
        
        # Find by acronym
        found3 = filled_keyword_list.find_keyword("JS")
        assert found3 is not None
        assert found3.keyword == "javascript"
        
        # Find nonexistent term
        found4 = filled_keyword_list.find_keyword("nonexistent")
        assert found4 is None
    
    def test_merge(self):
        """Test merging two keyword lists."""
        kw_list1 = KeywordList.from_list(["first", "second"])
        kw_list2 = KeywordList.from_list(["third", "fourth"])
        
        kw_list1.merge(kw_list2)
        all_keywords = kw_list1.get_all_keywords()
        
        assert len(kw_list1) == 4
        assert "first" in all_keywords
        assert "second" in all_keywords
        assert "third" in all_keywords
        assert "fourth" in all_keywords
        
        # Test merging with duplicates
        kw_list3 = KeywordList.from_list(["second", "fifth"])
        kw_list1.merge(kw_list3)
        
        assert len(kw_list1) == 5  # Should not add duplicate "second"
        assert "fifth" in kw_list1.get_all_keywords()
    
    def test_related_terms_property(self, filled_keyword_list):
        """Test the related_terms property."""
        terms = filled_keyword_list.related_terms
        
        # Check all terms are included
        assert "python" in terms
        assert "snake" in terms
        assert "anaconda" in terms
        assert "PY" in terms
        assert "javascript" in terms
        assert "js" in terms
        assert "ecmascript" in terms
        assert "JS" in terms
        
        # Test cache invalidation when adding a new keyword
        kw_new = Keyword("new")
        kw_new.add_synonyms(["fresh"])
        
        filled_keyword_list.add_keyword(kw_new)
        updated_terms = filled_keyword_list.related_terms
        
        assert "new" in updated_terms
        assert "fresh" in updated_terms
    
    def test_iteration(self, filled_keyword_list):
        """Test iterating over keywords."""
        keywords = []
        for kw in filled_keyword_list:
            keywords.append(kw.keyword)
        
        assert len(keywords) == 2
        assert "python" in keywords
        assert "javascript" in keywords
    
    def test_indexing(self, filled_keyword_list):
        """Test accessing keywords by index."""
        # Test direct indexing
        assert filled_keyword_list[0].keyword in ["python", "javascript"]
        assert filled_keyword_list[1].keyword in ["python", "javascript"]
        assert filled_keyword_list[0].keyword != filled_keyword_list[1].keyword
        
        # Test slicing
        slice_list = filled_keyword_list[0:1]
        assert len(slice_list) == 1
        assert slice_list[0].keyword in ["python", "javascript"]
        
        # Test out of bounds
        with pytest.raises(IndexError):
            filled_keyword_list[99]
    
    def test_len(self, empty_keyword_list, filled_keyword_list):
        """Test getting the length of keyword lists."""
        assert len(empty_keyword_list) == 0
        assert len(filled_keyword_list) == 2
    
    def test_equality(self):
        """Test equality comparison between keyword lists."""
        kw_list1 = KeywordList.from_list(["a", "b", "c"])
        kw_list2 = KeywordList.from_list(["a", "b", "c"])
        kw_list3 = KeywordList.from_list(["a", "b", "d"])
        
        assert kw_list1 == kw_list2
        assert kw_list1 != kw_list3
        assert kw_list1 != "not a keyword list"
        
        # Test with different order
        kw_list4 = KeywordList.from_list(["c", "a", "b"])
        assert kw_list1 == kw_list4  # Should be equal regardless of order
    
    def test_contains(self, filled_keyword_list):
        """Test checking if a term is in the keyword list."""
        # Test primary keywords
        assert "python" in filled_keyword_list
        assert "javascript" in filled_keyword_list
        
        # Test synonyms and acronyms
        assert "snake" in filled_keyword_list
        assert "JS" in filled_keyword_list
        
        # Test nonexistent term
        assert "nonexistent" not in filled_keyword_list
    
    def test_repr(self, filled_keyword_list):
        """Test the repr method."""
        repr_str = repr(filled_keyword_list)
        assert "KeywordList" in repr_str
        assert "keywords=" in repr_str