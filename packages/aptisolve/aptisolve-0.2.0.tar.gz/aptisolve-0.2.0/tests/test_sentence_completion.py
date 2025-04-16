import pytest
from verbalapt import sentence_completion

def test_sentence_completion():
    # Test adding a sentence completion question
    sentence_completion.add_question(
        sentence="The sky is ___.",
        missing_word="blue",
        options=["blue", "green", "red", "yellow"],
        explanation="The sky appears blue due to Rayleigh scattering."
    )
    
    # Get a random question
    question = sentence_completion.get_random_question()
    
    # Test that we can get a question
    assert question is not None
    
    # Test checking a correct answer
    if question["missing_word"] == "blue":
        result = sentence_completion.check_answer(question, "blue")
        assert result["correct"] == True
        assert "Correct" in result["feedback"]
    
    # Test checking an incorrect answer
    result = sentence_completion.check_answer(question, "green")
    assert result["correct"] == False
    assert "Incorrect" in result["feedback"]