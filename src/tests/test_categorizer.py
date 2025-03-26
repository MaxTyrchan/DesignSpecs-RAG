import pytest
from services.categorizer import categorize

# Sample mock class to simulate elements with a to_dict() method
class MockElement:
    def __init__(self, type_value):
        self.type_value = type_value

    def to_dict(self):
        return {"type": self.type_value}

def test_categorize_valid_input():
    # Create a list of mock elements with different 'type' values
    elements = [MockElement("table"), MockElement("text"), MockElement("table")]
    
    # Expected output is a set of unique types
    expected_output = {"table", "text"}

    # Assert the categorize function returns the correct unique types
    assert categorize(elements) == expected_output

def test_categorize_invalid_input():
    # Provide invalid input (not a list)
    invalid_input = {"type": "fruit"}

    # Assert that ValueError is raised for invalid input type
    with pytest.raises(ValueError, match="elements must be a dictionary"):
        categorize(invalid_input)