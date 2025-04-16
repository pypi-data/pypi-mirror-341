from typing import List, Dict, Union
from .utils import load_questions, save_questions

def add_passage(passage_text: str, questions: List[Dict]) -> Dict[str, Union[str, List[str]]]:
    """
    Add a new reading comprehension passage with questions
    
    Args:
        passage_text: The text of the passage
        questions: List of question dictionaries, each containing:
            - question: The question text
            - options: List of possible answers
            - correct_answer: The correct answer
            - explanation: Explanation of the answer
    """
    steps = []
    steps.append("Adding new reading comprehension passage")
    steps.append(f"Passage length: {len(passage_text)} characters")
    steps.append(f"Number of questions: {len(questions)}")
    
    # Validate questions format
    for i, question in enumerate(questions):
        if not all(key in question for key in ["question", "options", "correct_answer", "explanation"]):
            return {
                "status": "error",
                "message": f"Invalid question format at index {i}",
                "steps": steps
            }
    
    # Load existing passages
    passages = load_questions('reading_comprehension')
    
    # Add new passage
    passage_id = len(passages) + 1
    new_passage = {
        "id": passage_id,
        "text": passage_text,
        "questions": questions
    }
    
    passages.append(new_passage)
    save_questions('reading_comprehension', passages)
    
    steps.append("Passage and questions successfully added")
    
    return {
        "status": "success",
        "passage_id": passage_id,
        "steps": steps
    }

def get_passage(passage_id: int) -> Dict[str, Union[str, List[Dict]]]:
    """Get a specific passage and its questions"""
    passages = load_questions('reading_comprehension')
    
    for passage in passages:
        if passage["id"] == passage_id:
            return {
                "text": passage["text"],
                "questions": passage["questions"]
            }
    
    return {
        "error": "Passage not found"
    }

def get_random_passage() -> Dict[str, Union[str, List[Dict]]]:
    """Get a random passage for practice"""
    import random
    passages = load_questions('reading_comprehension')
    
    if not passages:
        return {
            "error": "No passages available"
        }
    
    passage = random.choice(passages)
    
    # Return with the expected key name
    return {
        "passage_text": passage["text"],
        "questions": passage["questions"],
        "id": passage["id"]
    }


def check_answer(question: Dict, user_answer: str) -> Dict[str, Union[bool, str]]:
    """
    Check if the user's answer is correct for a reading comprehension question
    
    Args:
        question: The question dictionary
        user_answer: The user's answer
        
    Returns:
        Dictionary with results
    """
    # If options are provided and user entered a letter
    if question['options'] and user_answer.upper() in "ABCDEFGH":
        answer_index = ord(user_answer.upper()) - ord('A')
        if 0 <= answer_index < len(question['options']):
            user_answer = question['options'][answer_index]
    
    is_correct = user_answer.lower() == question['correct_answer'].lower()
    
    if is_correct:
        feedback = f"Correct! {question.get('explanation', '')}"
    else:
        feedback = f"Incorrect. The correct answer is '{question['correct_answer']}'. {question.get('explanation', '')}"
    
    return {
        "correct": is_correct,
        "feedback": feedback
    }