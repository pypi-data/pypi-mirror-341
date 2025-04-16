import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from verbalapt import para_jumbles

def test_para_jumbles():
    # Test adding a paragraph jumble question
    para_jumbles.add_question(
        sentences=[
            "The sun was setting behind the mountains.",
            "It was a beautiful evening in the countryside.",
            "Birds were returning to their nests.",
            "The sky was painted with hues of orange and purple."
        ],
        correct_order=[1, 0, 3, 2],
        explanation="The paragraph starts with setting the scene, then describes the sunset and sky, and ends with the birds."
    )
    
    # Get a random question
    question = para_jumbles.get_random_question()
    
    # Test that we can get a question
    assert question is not None
    
    # Test checking a correct answer
    correct_sequence = ''.join([chr(65 + i) for i in question['correct_order']])
    result = para_jumbles.check_answer(question, correct_sequence)
    assert result["correct"] == True
    assert "Correct" in result["feedback"]
    
    # Test checking an incorrect answer
    incorrect_sequence = 'ABCD'  # This is likely incorrect unless by chance
    if incorrect_sequence != correct_sequence:
        result = para_jumbles.check_answer(question, incorrect_sequence)
        assert result["correct"] == False
        assert "Incorrect" in result["feedback"]