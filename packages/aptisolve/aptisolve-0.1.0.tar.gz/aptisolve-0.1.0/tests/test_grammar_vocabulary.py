import pytest
from verbalapt import grammar_vocabulary

def test_grammar_vocabulary():
    # Test adding a grammar question
    grammar_vocabulary.add_question(
        question_text="Which sentence is grammatically correct?",
        options=[
            "She don't like ice cream.",
            "She doesn't like ice cream.",
            "She not like ice cream.",
            "She do not likes ice cream."
        ],
        correct_answer="She doesn't like ice cream.",
        explanation="The correct negative form of the third person singular is 'doesn't'.",
        category="grammar"
    )
    
    # Get a random question
    question = grammar_vocabulary.get_random_question("grammar")
    
    # Test that we can get a question
    assert question is not None
    
    # Test checking a correct answer
    if "She doesn't like ice cream." in question["options"]:
        result = grammar_vocabulary.check_answer(question, "She doesn't like ice cream.")
        assert result["correct"] == True
        assert "Correct" in result["feedback"]
    
    # Test checking an incorrect answer with letter
    if len(question["options"]) >= 2:
        # Find an incorrect option
        correct_answer = question["correct_answer"]
        incorrect_option = next(option for option in question["options"] if option != correct_answer)
        incorrect_index = question["options"].index(incorrect_option)
        incorrect_letter = chr(65 + incorrect_index)  # Convert to letter (A, B, C, etc.)
        
        result = grammar_vocabulary.check_answer(question, incorrect_letter)
        assert "Incorrect" in result["feedback"]