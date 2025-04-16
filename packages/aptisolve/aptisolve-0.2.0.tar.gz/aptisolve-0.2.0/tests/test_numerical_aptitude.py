import pytest
import math
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from numerical_aptitude.permutations_combinations import (
    calculate_factorial,
    calculate_permutation,
    calculate_combination,
    permutation_with_repetition,
    combination_with_repetition
)
from numerical_aptitude.probability import (
    calculate_probability,
    calculate_compound_probability,
    calculate_conditional_probability,
    calculate_bayes_theorem
)

class TestPermutationsCombinations:
    def test_calculate_factorial(self):
        # Test factorial of 0
        result = calculate_factorial(0)
        assert result["answer"] == 1
        
        # Test factorial of 5
        result = calculate_factorial(5)
        assert result["answer"] == 120
        
        # Test error case
        result = calculate_factorial(-1)
        assert "Error" in result["answer"]
    
    def test_calculate_permutation(self):
        # Test P(5,3)
        result = calculate_permutation(5, 3)
        assert result["answer"] == 60  # 5!/(5-3)! = 5!/2! = 120/2 = 60
        
        # Test error cases
        result = calculate_permutation(-1, 3)
        assert "Error" in result["answer"]
        
        result = calculate_permutation(3, 5)
        assert "Error" in result["answer"]
    
    def test_calculate_combination(self):
        # Test C(5,3)
        result = calculate_combination(5, 3)
        assert result["answer"] == 10  # 5!/(3!*(5-3)!) = 5!/(3!*2!) = 120/(6*2) = 10
        
        # Test error cases
        result = calculate_combination(-1, 3)
        assert "Error" in result["answer"]
        
        result = calculate_combination(3, 5)
        assert "Error" in result["answer"]
    
    def test_permutation_with_repetition(self):
        # Test P(3,2) with repetition
        result = permutation_with_repetition(3, 2)
        assert result["answer"] == 9  # 3^2 = 9
        
        # Test error case
        result = permutation_with_repetition(-1, 2)
        assert "Error" in result["answer"]
    
    def test_combination_with_repetition(self):
        # Test C(3,2) with repetition
        result = combination_with_repetition(3, 2)
        assert result["answer"] == 6  # (3+2-1)!/(2!*(3-1)!) = 4!/(2!*2!) = 24/(4) = 6
        
        # Test error case
        result = combination_with_repetition(-1, 2)
        assert "Error" in result["answer"]

class TestProbability:
    def test_calculate_probability(self):
        # Test probability of getting a head when flipping a coin
        result = calculate_probability(1, 2)
        assert result["answer"] == 0.5
        assert result["fraction"] == "1/2"
        assert result["percentage"] == "50.00%"
        
        # Test error cases
        result = calculate_probability(3, 2)
        assert "Error" in result["answer"]
        
        result = calculate_probability(1, 0)
        assert "Error" in result["answer"]
    
    def test_calculate_compound_probability(self):
        # Test AND operation
        result = calculate_compound_probability(0.5, 0.6, "and")
        assert result["answer"] == 0.3  # 0.5 * 0.6 = 0.3
        
        # Test OR operation
        result = calculate_compound_probability(0.5, 0.6, "or")
        assert result["answer"] == 0.8  # 0.5 + 0.6 - (0.5 * 0.6) = 0.8
        
        # Test error cases
        result = calculate_compound_probability(1.5, 0.6, "and")
        assert "Error" in result["answer"]
        
        result = calculate_compound_probability(0.5, 0.6, "invalid")
        assert "Error" in result["answer"]
    
    def test_calculate_conditional_probability(self):
        # Test P(A and B) = P(A) * P(B|A)
        result = calculate_conditional_probability(0.5, 0.6)
        assert result["answer"] == 0.3  # 0.5 * 0.6 = 0.3
        
        # Test error case
        result = calculate_conditional_probability(1.5, 0.6)
        assert "Error" in result["answer"]
    
    def test_calculate_bayes_theorem(self):
        # Test Bayes' Theorem
        # P(A|B) = [P(B|A) * P(A)] / [P(B|A) * P(A) + P(B|not A) * P(not A)]
        result = calculate_bayes_theorem(0.3, 0.8, 0.2)
        # P(A|B) = (0.8 * 0.3) / [(0.8 * 0.3) + (0.2 * 0.7)]
        # = 0.24 / (0.24 + 0.14) = 0.24 / 0.38 = 0.6316...
        assert abs(result["answer"] - 0.6316) < 0.001
        
        # Test error case
        result = calculate_bayes_theorem(1.5, 0.8, 0.2)
        assert "Error" in result["answer"]