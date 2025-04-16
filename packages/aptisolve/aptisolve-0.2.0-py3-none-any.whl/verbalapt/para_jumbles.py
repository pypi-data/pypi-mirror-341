from typing import Dict, List, Union
import random
from .utils import load_questions, save_questions, evaluate_performance, get_user_input

def add_question(sentences: List[str], correct_order: List[int], explanation: str = "") -> None:
    """
    Add a new paragraph jumble question.
    
    Parameters:
    - sentences: List of sentences in jumbled order
    - correct_order: List of indices showing the correct order (0-based)
    - explanation: Explanation of the logical flow
    """
    questions = load_questions('para_jumbles')
    
    questions.append({
        "sentences": sentences,
        "correct_order": correct_order,
        "explanation": explanation
    })
    
    save_questions('para_jumbles', questions)

def get_random_question() -> Dict:
    """Get a random paragraph jumble question."""
    questions = load_questions('para_jumbles')
    if not questions:
        return None
    return random.choice(questions)

def display_question(question: Dict) -> None:
    """Display a paragraph jumble question to the user."""
    print("\nArrange the following sentences in the correct order:\n")
    for i, sentence in enumerate(question['sentences']):
        print(f"  {chr(65+i)}. {sentence}")
    
    print("\nEnter the correct sequence (e.g., BDCA):")

def check_answer(question: Dict, user_answer: str) -> Dict[str, Union[bool, str]]:
    """Check if the user's answer is correct and provide feedback."""
    # Convert user's letter sequence to indices
    user_order = []
    for char in user_answer.upper():
        if 'A' <= char <= 'Z':
            user_order.append(ord(char) - ord('A'))
    
    is_correct = user_order == question['correct_order']
    
    # Create the correct sequence as letters
    correct_sequence = ''.join([chr(65 + i) for i in question['correct_order']])
    
    if is_correct:
        feedback = f"Correct! The right sequence is {correct_sequence}. " + question.get('explanation', '')
    else:
        feedback = f"Incorrect. The correct sequence is {correct_sequence}. " + question.get('explanation', '')
        
        # Show the paragraph in correct order
        feedback += "\n\nCorrect paragraph:"
        for i in question['correct_order']:
            feedback += f"\n{question['sentences'][i]}"
    
    return {
        "correct": is_correct,
        "feedback": feedback
    }

def practice_session(num_questions: int = 3) -> Dict:
    """Run an interactive paragraph jumble practice session."""
    correct_count = 0
    
    for i in range(num_questions):
        question = get_random_question()
        if not question:
            print("No questions available. Please add some questions first.")
            break
        
        display_question(question)
        user_answer = get_user_input("Your answer: ")
        
        result = check_answer(question, user_answer)
        print(result["feedback"])
        
        if result["correct"]:
            correct_count += 1
    
    return evaluate_performance(correct_count, num_questions)