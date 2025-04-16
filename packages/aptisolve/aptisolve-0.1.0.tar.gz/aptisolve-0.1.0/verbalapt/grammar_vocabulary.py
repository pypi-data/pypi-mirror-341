from typing import Dict, List, Union
import random
from .utils import load_questions, save_questions, evaluate_performance, get_user_input

def add_question(question_text: str, options: List[str], correct_answer: str, explanation: str = "", category: str = "grammar") -> None:
    """
    Add a new grammar or vocabulary question.
    
    Parameters:
    - question_text: The question
    - options: List of possible answers
    - correct_answer: The correct option
    - explanation: Why this is the correct answer
    - category: 'grammar' or 'vocabulary'
    """
    questions = load_questions(f'{category}_questions')
    
    questions.append({
        "question_text": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "category": category
    })
    
    save_questions(f'{category}_questions', questions)

def get_random_question(category: str = None) -> Dict:
    """Get a random grammar or vocabulary question."""
    if category == "grammar":
        questions = load_questions('grammar_questions')
    elif category == "vocabulary":
        questions = load_questions('vocabulary_questions')
    else:
        # Combine both types
        questions = load_questions('grammar_questions') + load_questions('vocabulary_questions')
    
    if not questions:
        return None
    
    return random.choice(questions)

def display_question(question: Dict, question_num: int) -> None:
    """Display a question with multiple choice options."""
    print(f"\nQuestion {question_num}: {question['question_text']}")
    for i, option in enumerate(question['options']):
        print(f"  {chr(65+i)}. {option}")

def check_answer(question: Dict, user_answer: str) -> Dict[str, Union[bool, str]]:
    """Check if the user's answer is correct and provide feedback."""
    # Convert letter answer (A, B, C, D) to option text
    if user_answer.upper() in "ABCDEFGH":
        answer_index = ord(user_answer.upper()) - ord('A')
        if 0 <= answer_index < len(question['options']):
            user_answer = question['options'][answer_index]
    
    is_correct = user_answer.lower() == question['correct_answer'].lower()
    
    if is_correct:
        feedback = "Correct! " + question.get('explanation', '')
    else:
        feedback = f"Incorrect. The correct answer is: {question['correct_answer']}. " + question.get('explanation', '')
    
    return {
        "correct": is_correct,
        "feedback": feedback
    }

def practice_session(num_questions: int = 5, category: str = None) -> Dict:
    """Run an interactive grammar/vocabulary practice session."""
    correct_count = 0
    
    for i in range(num_questions):
        question = get_random_question(category)
        if not question:
            print(f"No {category if category else 'grammar/vocabulary'} questions available. Please add some questions first.")
            break
        
        display_question(question, i+1)
        user_answer = get_user_input("Your answer (A, B, C, D or type the full answer): ")
        
        result = check_answer(question, user_answer)
        print(result["feedback"])
        
        if result["correct"]:
            correct_count += 1
    
    return evaluate_performance(correct_count, num_questions)