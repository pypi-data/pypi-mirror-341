"""
Test initialization file for improving test coverage.
This file contains additional tests for modules with low coverage.
"""

import pytest
import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules that need improved coverage
from numerical_aptitude import (
    algebra, 
    averages, 
    mixtures_alligations, 
    number_system,
    number_systems,
    ratios_proportions,
    time_speed_distance,
    time_work
)

from logical_reasoning import (
    analogy,
    blood_relations,
    coding_decoding,
    direction_sense,
    number_series,
    puzzles,
    statement_conclusion
)

from verbalapt import (
    grammar_vocabulary,
    one_word_substitution,
    para_jumbles,
    reading_comprehension,
    sentence_completion,
    utils
)

# Test numerical_aptitude modules with low coverage
def test_algebra():
    # Test solving linear equation
    result = algebra.solve_linear_equation("2x + 3 = 7")
    assert result["answer"] == 2
    assert len(result["steps"]) > 0
    
    # Test solving quadratic equation
    result = algebra.solve_quadratic_equation(1, -3, 2)
    assert 1 in result["answers"]
    assert 2 in result["answers"]
    assert len(result["steps"]) > 0

def test_averages():
    # Test calculating average
    result = averages.calculate_average([10, 20, 30, 40, 50])
    assert result["answer"] == 30
    assert len(result["steps"]) > 0
    
    # Test weighted average
    result = averages.calculate_weighted_average([80, 90, 75], [0.3, 0.5, 0.2])
    assert abs(result["answer"] - 84.0) < 0.01
    assert len(result["steps"]) > 0

def test_mixtures_alligations():
    # Test mixture problems
    result = mixtures_alligations.calculate_mixture_ratio(40, 60, 50)
    assert result["ratio"] == "1:1"
    assert len(result["steps"]) > 0
    
    # Test alligation problems
    result = mixtures_alligations.calculate_mean_price(100, 20, 1, 2)
    assert abs(result["mean_price"] - 40.0) < 0.01
    assert len(result["steps"]) > 0

def test_number_system():
    # Test number conversion
    result = number_system.convert_base(10, 2)
    assert result["answer"] == "1010"
    assert len(result["steps"]) > 0
    
    # Test LCM and HCF
    result = number_system.find_lcm_hcf(12, 18)
    assert result["lcm"] == 36
    assert result["hcf"] == 6
    assert len(result["steps"]) > 0

def test_ratios_proportions():
    # Test ratio calculation
    result = ratios_proportions.calculate_ratio(15, 25)
    assert result["simplified_ratio"] == "3:5"
    assert len(result["steps"]) > 0
    
    # Test proportion problems
    result = ratios_proportions.solve_proportion(2, 3, 8)
    assert result["answer"] == 12
    assert len(result["steps"]) > 0

def test_time_speed_distance():
    # Test speed calculation
    result = time_speed_distance.calculate_speed(120, 2)
    assert result["answer"] == 60
    assert len(result["steps"]) > 0
    
    # Test time calculation
    result = time_speed_distance.calculate_time(240, 60)
    assert result["answer"] == 4
    assert len(result["steps"]) > 0

def test_time_work():
    # Test work problems
    result = time_work.calculate_work_time(10, 15)
    assert result["answer"] == 6
    assert len(result["steps"]) > 0
    
    # Test efficiency problems
    result = time_work.calculate_efficiency(12, 3)
    assert result["answer"] == 4
    assert len(result["steps"]) > 0

# Test logical_reasoning modules with low coverage
def test_analogy():
    # Test solving analogy
    result = analogy.solve_analogy("Hand is to Glove as Foot is to", ["Sock", "Shoe", "Leg", "Toe"])
    assert result["answer"] == "Shoe"
    assert len(result["steps"]) > 0
    
    # Test finding relationship
    result = analogy.find_relationship("Doctor", "Patient")
    assert "relationship" in result
    assert len(result["steps"]) > 0

def test_number_series():
    # Test arithmetic progression
    result = number_series.identify_pattern([2, 4, 6, 8, 10])
    assert "arithmetic" in result["pattern"].lower()
    assert result["next_number"] == 12
    assert len(result["steps"]) > 0
    
    # Test geometric progression
    result = number_series.identify_pattern([2, 4, 8, 16, 32])
    assert "geometric" in result["pattern"].lower()
    assert result["next_number"] == 64
    assert len(result["steps"]) > 0

def test_puzzles():
    # Test seating arrangement
    result = puzzles.solve_seating_arrangement(
        ["A sits to the right of B", "C sits to the left of B", "D sits opposite to A"],
        ["A", "B", "C", "D"]
    )
    assert isinstance(result["arrangement"], dict)
    assert len(result["steps"]) > 0

# Test verbalapt modules with low coverage
def test_one_word_substitution():
    # Test adding a word
    one_word_substitution.add_word(
        word="Bibliophile",
        meaning="A person who loves books",
        example="As a bibliophile, she has an extensive collection of rare books."
    )
    
    # Test getting a word
    word = one_word_substitution.get_word("Bibliophile")
    assert word is not None
    assert word["meaning"] == "A person who loves books"
    
    # Test getting a random word
    random_word = one_word_substitution.get_random_word()
    assert random_word is not None
    assert "word" in random_word
    assert "meaning" in random_word

def test_reading_comprehension():
    # Test adding a passage
    reading_comprehension.add_passage(
        passage_text="The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet.",
        questions=[
            {
                "question": "What animal jumps in the passage?",
                "options": ["Dog", "Fox", "Cat", "Wolf"],
                "correct_answer": "Fox",
                "explanation": "The passage states 'The quick brown fox jumps over the lazy dog.'"
            }
        ]
    )
    
    # Test getting a passage
    passage = reading_comprehension.get_random_passage()
    assert passage is not None
    assert "passage_text" in passage
    assert "questions" in passage
    
    # Test checking an answer
    if passage and passage["questions"]:
        question = passage["questions"][0]
        result = reading_comprehension.check_answer(question, question["correct_answer"])
        assert result["correct"] == True
        assert "feedback" in result

def test_utils():
    # Test word similarity
    similarity = utils.calculate_word_similarity("happy", "joyful")
    assert 0 <= similarity <= 1
    
    # Test sentence complexity
    complexity = utils.calculate_sentence_complexity("This is a simple sentence.")
    assert complexity >= 0
    
    # Test word frequency
    frequency = utils.get_word_frequency("the")
    assert frequency > 0