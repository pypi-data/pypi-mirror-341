import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the correct functions based on what's available in the modules
from logical_reasoning.blood_relations import solve_blood_relation
from logical_reasoning.number_series import identify_pattern
from logical_reasoning.direction_sense import solve_direction_problem
from logical_reasoning.coding_decoding import decode_message
from logical_reasoning.puzzles import solve_seating_arrangement  # Changed from solve_puzzle
from logical_reasoning.syllogisms import analyze_syllogism
from logical_reasoning.statement_conclusion import analyze_statement_conclusion
from logical_reasoning.analogy import solve_analogy

class TestBloodRelations:
    def test_solve_blood_relation(self):
        result = solve_blood_relation("A is the father of B", "B")
        assert isinstance(result, dict)
        assert "answer" in result  # Changed from "relationship"
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert "practice_tip" in result  # Added this assertion

class TestNumberSeries:
    def test_identify_pattern(self):
        # Test arithmetic progression
        result = identify_pattern([2, 4, 6, 8, 10])
        assert isinstance(result, dict)
        assert "pattern" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        
        # Test geometric progression
        result = identify_pattern([2, 4, 8, 16, 32])
        assert isinstance(result, dict)
        assert "pattern" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)

class TestDirectionSense:
    def test_solve_direction_problem(self):
        result = solve_direction_problem(
            "Point A", 
            ["Walk 2 steps North", "Turn right", "Walk 3 steps East"]
        )
        assert isinstance(result, dict)
        assert "final_position" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)

class TestCodingDecoding:
    def test_decode_message(self):
        result = decode_message("IFMMP", "shift cipher with shift value 1")
        assert isinstance(result, dict)
        assert "decoded_message" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)

class TestPuzzles:
    def test_solve_seating_arrangement(self):  # Changed from test_solve_puzzle
        clues = [
            "Five friends A, B, C, D, and E are sitting in a row facing north.",
            "A sits at one of the ends.",
            "B sits next to C.",
            "D sits next to E.",
            "C sits in the middle."
        ]
        result = solve_seating_arrangement(clues)  # Changed from solve_puzzle
        assert isinstance(result, dict)
        assert "arrangement" in result  # Changed from "steps"
        assert "steps" in result
        assert isinstance(result["steps"], list)

class TestSyllogisms:
    def test_analyze_syllogism(self):
        premises = ["All dogs are animals", "All animals need food"]
        conclusion = "All dogs need food"
        result = analyze_syllogism(premises, conclusion)
        assert isinstance(result, dict)
        assert "valid" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)

class TestStatementConclusion:
    def test_analyze_statement_conclusion(self):
        statement = "All fruits are sweet. All sweet things are tasty."
        conclusions = ["All fruits are tasty", "Some tasty things are fruits"]
        result = analyze_statement_conclusion(statement, conclusions)
        assert isinstance(result, dict)
        assert "follows" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)

class TestAnalogy:
    def test_solve_analogy(self):
        result = solve_analogy(["Hand", "Glove"], "Foot")
        assert isinstance(result, dict)
        assert "answer" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)