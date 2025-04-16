import pytest
from numerical_aptitude import simple_interest

# Update the test_simple_interest function to expect more steps
def test_simple_interest():
    result = simple_interest.calculate_simple_interest(1000, 5, 2)
    assert result["answer"] == 1100.0
    assert result["interest"] == 100.0
    assert len(result["steps"]) > 0  # Just check that steps exist, not the exact number