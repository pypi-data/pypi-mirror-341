from typing import Dict, List, Union
import random
from .utils import load_questions, save_questions, evaluate_performance, get_user_input

# Dictionary to store word substitutions
word_database = {}

def add_word(word: str, meaning: str, example: str) -> Dict[str, Union[str, List[str]]]:
    """
    Add a new word with its meaning and example to the one-word substitution database
    """
    steps = []
    steps.append(f"Adding new word: {word}")
    steps.append(f"Meaning: {meaning}")
    steps.append(f"Example: {example}")
    
    # Add to database
    word_database[word] = {
        "meaning": meaning,
        "example": example
    }
    
    steps.append("Word successfully added to package")
    
    return {
        "status": "success",
        "word": word,
        "steps": steps
    }

def find_word(meaning: str) -> Dict[str, Union[str, List[str]]]:
    """
    Find a word based on its meaning
    """
    steps = []
    steps.append(f"Searching for word with meaning: {meaning}")
    
    matching_words = []
    for word, details in word_database.items():
        if meaning.lower() in details["meaning"].lower():
            matching_words.append(word)
    
    if matching_words:
        steps.append(f"Found {len(matching_words)} matching word(s)")
        return {
            "words": matching_words,
            "steps": steps
        }
    
    steps.append("No matching words found")
    return {
        "words": [],
        "steps": steps
    }

def get_example(word: str) -> Dict[str, Union[str, List[str]]]:
    """
    Get the example usage of a word
    """
    steps = []
    steps.append(f"Looking up example for: {word}")
    
    if word in word_database:
        example = word_database[word]["example"]
        steps.append(f"Example found: {example}")
        return {
            "example": example,
            "steps": steps
        }
    
    steps.append("Word not found in package")
    return {
        "example": None,
        "steps": steps
    }

def add_question(phrase: str, word: str, options: List[str] = None, explanation: str = "") -> None:
    """
    Add a new one-word substitution question.
    
    Parameters:
    - phrase: The phrase or definition
    - word: The single word that replaces the phrase
    - options: List of possible answers (including the correct one)
    - explanation: Additional explanation
    """
    questions = load_questions('one_word_substitution')
    
    questions.append({
        "phrase": phrase,
        "word": word,
        "options": options if options else [],
        "explanation": explanation
    })
    
    save_questions('one_word_substitution', questions)

def get_random_question() -> Dict:
    """Get a random one-word substitution question."""
    questions = load_questions('one_word_substitution')
    if not questions:
        return None
    return random.choice(questions)

def display_question(question: Dict, question_num: int) -> None:
    """Display a one-word substitution question."""
    print(f"\nQuestion {question_num}: What is one word for '{question['phrase']}'?")
    
    if question['options']:
        for i, option in enumerate(question['options']):
            print(f"  {chr(65+i)}. {option}")

def check_answer(question: Dict, user_answer: str) -> Dict[str, Union[bool, str]]:
    """Check if the user's answer is correct and provide feedback."""
    # If options are provided and user entered a letter
    if question['options'] and user_answer.upper() in "ABCDEFGH":
        answer_index = ord(user_answer.upper()) - ord('A')
        if 0 <= answer_index < len(question['options']):
            user_answer = question['options'][answer_index]
    
    is_correct = user_answer.lower() == question['word'].lower()
    
    if is_correct:
        feedback = f"Correct! '{question['word']}' is the word for '{question['phrase']}'. " + question.get('explanation', '')
    else:
        feedback = f"Incorrect. The correct word is '{question['word']}' for '{question['phrase']}'. " + question.get('explanation', '')
    
    return {
        "correct": is_correct,
        "feedback": feedback
    }

def practice_session(num_questions: int = 5) -> Dict:
    """Run an interactive one-word substitution practice session."""
    correct_count = 0
    
    for i in range(num_questions):
        question = get_random_question()
        if not question:
            print("No questions available. Please add some questions first.")
            break
        
        display_question(question, i+1)
        
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


def get_random_word() -> Dict[str, Union[str, List[str]]]:
    """
    Get a random word from the one-word substitution database
    """
    import random
    
    steps = []
    steps.append("Retrieving a random word from the database")
    
    if not word_database:
        steps.append("Database is empty")
        return {
            "error": "No words in database",
            "steps": steps
        }
    
    random_word = random.choice(list(word_database.keys()))
    details = word_database[random_word]
    
    steps.append(f"Selected word: {random_word}")
    
    return {
        "word": random_word,
        "meaning": details["meaning"],
        "example": details["example"],
        "steps": steps
    }

def get_word(word: str) -> Dict[str, Union[str, List[str]]]:
    """
    Get the details of a word from the one-word substitution database
    """
    steps = []
    steps.append(f"Looking up word: {word}")
    
    if word in word_database:
        details = word_database[word]
        steps.append("Word found in database")
        steps.append(f"Meaning: {details['meaning']}")
        steps.append(f"Example: {details['example']}")
        
        return {
            "word": word,
            "meaning": details["meaning"],
            "example": details["example"],
            "steps": steps
        }
    
    steps.append("Word not found in database")
    return {
        "error": "Word not found",
        "steps": steps
    }