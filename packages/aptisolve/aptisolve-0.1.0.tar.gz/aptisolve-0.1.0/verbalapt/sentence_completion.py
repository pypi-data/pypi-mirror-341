from typing import Dict, List, Union
import random
from .utils import load_questions, save_questions, evaluate_performance, get_user_input

def add_question(sentence: str, missing_word: str, options: List[str] = None, explanation: str = "") -> None:
    """
    Add a new sentence completion question.
    
    Parameters:
    - sentence: The sentence with a blank (use ___ for the blank)
    - missing_word: The correct word that fits in the blank
    - options: List of possible answers (including the correct one)
    - explanation: Why this is the correct answer
    """
    questions = load_questions('sentence_completion')
    
    questions.append({
        "sentence": sentence,
        "missing_word": missing_word,
        "options": options if options else [],
        "explanation": explanation
    })
    
    save_questions('sentence_completion', questions)

def get_random_question() -> Dict:
    """Get a random sentence completion question."""
    questions = load_questions('sentence_completion')
    if not questions:
        return None
    return random.choice(questions)

def display_question(question: Dict) -> None:
    """Display a sentence completion question to the user."""
    print(f"\nComplete the following sentence:\n")
    print(question['sentence'])
    
    if question['options']:
        print("\nOptions:")
        for i, option in enumerate(question['options']):
            print(f"  {chr(65+i)}. {option}")

def check_answer(question: Dict, user_answer: str) -> Dict[str, Union[bool, str]]:
    """Check if the user's answer is correct and provide feedback."""
    # If options are provided and user entered a letter
    if question['options'] and user_answer.upper() in "ABCDEFGH":
        answer_index = ord(user_answer.upper()) - ord('A')
        if 0 <= answer_index < len(question['options']):
            user_answer = question['options'][answer_index]
    
    is_correct = user_answer.lower() == question['missing_word'].lower()
    
    if is_correct:
        feedback = "Correct! " + question.get('explanation', '')
    else:
        feedback = f"Incorrect. The correct answer is: {question['missing_word']}. " + question.get('explanation', '')
    
    return {
        "correct": is_correct,
        "feedback": feedback
    }

def practice_session(num_questions: int = 5) -> Dict:
    """Run an interactive sentence completion practice session."""
    correct_count = 0
    
    for i in range(num_questions):
        question = get_random_question()
        if not question:
            print("No questions available. Please add some questions first.")
            break
        
        display_question(question)
        
        if question['options']:
            prompt = "Your answer (enter the letter or the word): "
        else:
            prompt = "Your answer: "
            
        user_answer = get_user_input(prompt)
        
        result = check_answer(question, user_answer)
        print(result["feedback"])
        
        if result["correct"]:
            correct_count += 1
    
    return evaluate_performance(correct_count, num_questions)