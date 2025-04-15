from keylex.matchers.keyword import Keyword
from .test_base import *


class TestKeyword:
    """Tests for the Keyword class."""
    
    def test_initialization(self):
        """Test basic initialization of Keyword objects."""
        kw = Keyword("test")
        assert kw.keyword == "test"
        assert len(kw.synonyms) == 0
        assert len(kw.acronyms) == 0
        assert kw.is_empty is True
    
    def test_add_synonyms(self, empty_keyword):
        """Test adding synonyms to a keyword."""
        empty_keyword.add_synonyms(["synonym1", "synonym2"])
        assert "synonym1" in empty_keyword.synonyms
        assert "synonym2" in empty_keyword.synonyms
        assert len(empty_keyword.synonyms) == 2
        
        # Test adding duplicate synonyms
        empty_keyword.add_synonyms(["synonym1", "synonym3"])
        assert len(empty_keyword.synonyms) == 3
        assert "synonym3" in empty_keyword.synonyms
    
    def test_remove_synonyms(self, filled_keyword):
        """Test removing synonyms from a keyword."""
        filled_keyword.remove_synonyms(["snake"])
        assert "snake" not in filled_keyword.synonyms
        assert "anaconda" in filled_keyword.synonyms
        
        # Test removing non-existent synonym
        filled_keyword.remove_synonyms(["nonexistent"])
        assert len(filled_keyword.synonyms) == 1
    
    def test_set_synonyms(self, filled_keyword):
        """Test setting all synonyms at once."""
        filled_keyword.set_synonyms(["new1", "new2"])
        assert len(filled_keyword.synonyms) == 2
        assert "snake" not in filled_keyword.synonyms
        assert "new1" in filled_keyword.synonyms
        assert "new2" in filled_keyword.synonyms
    
    def test_clear_synonyms(self, filled_keyword):
        """Test clearing all synonyms."""
        filled_keyword.clear_synonyms()
        assert len(filled_keyword.synonyms) == 0
    
    def test_add_acronyms(self, empty_keyword):
        """Test adding acronyms to a keyword."""
        empty_keyword.add_acronyms(["A1", "A2"])
        assert "A1" in empty_keyword.acronyms
        assert "A2" in empty_keyword.acronyms
        assert len(empty_keyword.acronyms) == 2
        
        # Test adding duplicate acronyms
        empty_keyword.add_acronyms(["A1", "A3"])
        assert len(empty_keyword.acronyms) == 3
        assert "A3" in empty_keyword.acronyms
    
    def test_remove_acronyms(self, filled_keyword):
        """Test removing acronyms from a keyword."""
        filled_keyword.remove_acronyms(["PY"])
        assert "PY" not in filled_keyword.acronyms
        assert "PYT" in filled_keyword.acronyms
        
        # Test removing non-existent acronym
        filled_keyword.remove_acronyms(["nonexistent"])
        assert len(filled_keyword.acronyms) == 1
    
    def test_set_acronyms(self, filled_keyword):
        """Test setting all acronyms at once."""
        filled_keyword.set_acronyms(["NEW1", "NEW2"])
        assert len(filled_keyword.acronyms) == 2
        assert "PY" not in filled_keyword.acronyms
        assert "NEW1" in filled_keyword.acronyms
        assert "NEW2" in filled_keyword.acronyms
    
    def test_clear_acronyms(self, filled_keyword):
        """Test clearing all acronyms."""
        filled_keyword.clear_acronyms()
        assert len(filled_keyword.acronyms) == 0
    
    def test_related_terms(self, filled_keyword):
        """Test the related_terms property."""
        related = filled_keyword.related_terms
        assert "python" in related
        assert "snake" in related
        assert "anaconda" in related
        assert "PY" in related
        assert "PYT" in related
        assert len(related) == 5
    
    def test_is_empty(self):
        """Test the is_empty property."""
        kw1 = Keyword("empty")
        assert kw1.is_empty is True
        
        kw2 = Keyword("not_empty")
        kw2.add_synonyms(["synonym"])
        assert kw2.is_empty is False
        
        kw3 = Keyword("not_empty2")
        kw3.add_acronyms(["NE"])
        assert kw3.is_empty is False
    
    def test_matches(self, filled_keyword):
        """Test the matches method."""
        assert filled_keyword.matches("python") is True
        assert filled_keyword.matches("snake") is True
        assert filled_keyword.matches("PY") is True
        assert filled_keyword.matches("unknown") is False
        
        # Test case sensitivity
        assert filled_keyword.matches("Python") is False
        assert filled_keyword.matches("SNAKE") is False
    
    def test_copy(self, filled_keyword):
        """Test creating a copy of a keyword."""
        copy = filled_keyword.copy()
        assert copy is not filled_keyword
        assert copy == filled_keyword
        assert copy.keyword == filled_keyword.keyword
        assert copy.synonyms == filled_keyword.synonyms
        assert copy.acronyms == filled_keyword.acronyms
        
        # Modify copy and check original is unchanged
        copy.add_synonyms(["new_synonym"])
        assert "new_synonym" in copy.synonyms
        assert "new_synonym" not in filled_keyword.synonyms
    
    def test_to_dict(self, filled_keyword):
        """Test serializing to dictionary."""
        data = filled_keyword.to_dict()
        assert data["keyword"] == "python"
        assert set(data["synonyms"]) == {"snake", "anaconda"}
        assert set(data["acronyms"]) == {"PY", "PYT"}
    
    def test_from_dict(self):
        """Test deserializing from dictionary."""
        data = {
            "keyword": "java",
            "synonyms": ["coffee", "jvm"],
            "acronyms": ["J"]
        }
        kw = Keyword.from_dict(data)
        assert kw.keyword == "java"
        assert "coffee" in kw.synonyms
        assert "jvm" in kw.synonyms
        assert "J" in kw.acronyms
        
        # Test with missing fields
        partial_data = {"keyword": "partial"}
        kw_partial = Keyword.from_dict(partial_data)
        assert kw_partial.keyword == "partial"
        assert len(kw_partial.synonyms) == 0
        assert len(kw_partial.acronyms) == 0
    
    def test_equality(self):
        """Test equality comparison between keywords."""
        kw1 = Keyword("same")
        kw1.add_synonyms(["synonym"])
        
        kw2 = Keyword("same")
        kw2.add_synonyms(["synonym"])
        
        kw3 = Keyword("different")
        
        assert kw1 == kw2
        assert kw1 != kw3
        assert kw1 != "not a keyword"
    
    def test_hash(self):
        """Test hashing of keywords."""
        kw1 = Keyword("hashable")
        kw1.add_synonyms(["synonym"])
        
        kw2 = Keyword("hashable")
        kw2.add_synonyms(["synonym"])
        
        kw3 = Keyword("different")
        
        # Same keywords should have same hash
        assert hash(kw1) == hash(kw2)
        
        # Test in a set
        keyword_set = {kw1, kw2, kw3}
        assert len(keyword_set) == 2
    
    def test_repr(self, filled_keyword):
        """Test the repr method."""
        repr_str = repr(filled_keyword)
        assert "Keyword" in repr_str
        assert "python" in repr_str
        assert "synonyms" in repr_str
        assert "acronyms" in repr_str
    
    def test_str(self, filled_keyword):
        """Test the str method."""
        str_repr = str(filled_keyword)
        assert "python" in str_repr
        assert "Synonyms: 2" in str_repr
        assert "Acronyms: 2" in str_repr