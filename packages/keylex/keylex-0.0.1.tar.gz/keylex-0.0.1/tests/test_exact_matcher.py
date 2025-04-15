# import pytest
# from keylex.matchers.exact_match import ExactMatcher
# from keylex.matchers.matcher import OutputFormat
# sample_text = "Python is great. I love python and PyThOn."

# @pytest.fixture
# def keywords():
#     return ["Python", "great"]

# def test_basic_match(keywords):
#     matcher = ExactMatcher(keywords)
#     matches = matcher.match(sample_text, output=OutputFormat.DETAILED.value)

#     assert isinstance(matches, list)
#     assert any(match['keyword'] == "Python" for match in matches)

# def test_case_sensitive_match(keywords):
#     matcher = ExactMatcher(keywords, case=True)
#     matches = matcher.match(sample_text, output=OutputFormat.KEYWORDS.value)

#     assert "Python" in matches
#     assert "great" in matches
#     assert all(match == "Python" or match == "great" for match in matches)

# def test_case_insensitive_match(keywords):
#     matcher = ExactMatcher(keywords, case=False)
#     matches = matcher.match(sample_text, output=OutputFormat.KEYWORDS.value)

#     assert "Python" in matches or "python" in matches
#     python_matches = [match for match in matches if match.lower() == "python"]
#     assert len(python_matches) >= 2

# # def test_output_boolean(keywords):
# #     matcher = ExactMatcher(keywords, case=False)
# #     output = matcher.match(sample_text, output=OutputFormat.BOOLEAN.value)

# #     assert isinstance(output, list)
# #     for item in output:
# #         assert isinstance(item, dict)
# #         for keyword in keywords:
# #             assert keyword in item
# #             assert isinstance(item[keyword], bool)

# def test_output_count(keywords):
#     matcher = ExactMatcher(keywords, case=False)
#     output = matcher.match(sample_text, output=OutputFormat.COUNT.value)

#     assert isinstance(output, dict)
#     for key in keywords:
#         assert key in output
#         assert isinstance(output[key], int)

# def test_no_match_case():
#     matcher = ExactMatcher(["nonexistent"], case=True)
#     output = matcher.match(sample_text, output=OutputFormat.KEYWORDS.value)

#     assert output == []

# def test_invalid_keywords_type():
#     with pytest.raises(ValueError, match="`keywords` must be a list of strings."):
#         ExactMatcher("notalist")

# def test_empty_keywords():
#     with pytest.raises(ValueError, match="`keywords` list cannot be empty."):
#         ExactMatcher([])

# def test_invalid_case_argument():
#     with pytest.raises(ValueError, match="`case` must be a boolean."):
#         ExactMatcher(["Python"], case="yes")

# def test_invalid_text_argument(keywords):
#     matcher = ExactMatcher(keywords)
#     with pytest.raises(ValueError, match="`text` must be a string."):
#         matcher.match(12345, output=OutputFormat.DETAILED.value)

# def test_invalid_output_format(keywords):
#     matcher = ExactMatcher(keywords)
#     with pytest.raises(ValueError, match="Invalid output format: invalid_format."):
#         matcher.match(sample_text, output="invalid_format")