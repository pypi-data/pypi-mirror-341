from hanjadict import lookup


def test_lookup_valid_character():
    """Test lookup with valid Hanja character."""
    result = lookup("雪")
    assert result == "눈 설"


def test_lookup_another_valid_character():
    """Test lookup with another valid character."""
    result = lookup("山")
    assert result == "메 산"  # Replace with actual expected result


def test_lookup_invalid_character():
    """Test lookup with invalid character."""
    result = lookup("xyz")
    assert result is None


def test_lookup_empty_string():
    """Test lookup with empty string."""
    result = lookup("")
    assert result is None
