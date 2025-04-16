from typing import Dict, Union, List
import json
import os
from difflib import SequenceMatcher

def calculate_word_similarity(word1: str, word2: str) -> float:
    """
    Calculate the similarity between two words using sequence matching
    Returns a float between 0 and 1, where 1 means identical
    """
    # Calculate similarity using SequenceMatcher
    similarity = SequenceMatcher(None, word1.lower(), word2.lower()).ratio()
    return similarity

def load_questions(category: str) -> List[Dict]:
    """Load questions from a JSON file"""
    file_path = os.path.join('data', f'{category}_questions.json')
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading questions: {e}")
    return []

def save_questions(category: str, questions: List[Dict]) -> None:
    """Save questions to a JSON file"""
    os.makedirs('data', exist_ok=True)
    file_path = os.path.join('data', f'{category}_questions.json')
    try:
        with open(file_path, 'w') as f:
            json.dump(questions, f, indent=4)
    except Exception as e:
        print(f"Error saving questions: {e}")

def evaluate_performance(correct: int, total: int) -> Dict[str, Union[int, float, str]]:
    """Evaluate performance and provide feedback"""
    if total == 0:
        return {
            "score": 0,
            "percentage": 0,
            "feedback": "No questions attempted"
        }
    
    percentage = (correct / total) * 100
    
    if percentage >= 90:
        feedback = "Excellent! Keep up the great work!"
    elif percentage >= 70:
        feedback = "Good job! With more practice, you can improve further."
    elif percentage >= 50:
        feedback = "Fair attempt. Regular practice will help you improve."
    else:
        feedback = "Keep practicing. You'll get better with time."
    
    return {
        "score": correct,
        "total": total,
        "percentage": percentage,
        "feedback": feedback
    }

def get_user_input(prompt: str) -> str:
    """Get and validate user input"""
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input:
                return user_input
            print("Please enter a valid response.")
        except KeyboardInterrupt:
            print("\nSession terminated by user.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")

def calculate_sentence_complexity(sentence: str) -> float:
    """
    Calculate the complexity of a sentence based on various metrics
    Returns a float representing the Flesch-Kincaid Grade Level
    """
    words = sentence.split()
    word_count = len(words)
    avg_word_length = sum(len(word) for word in words) / max(1, word_count)
    
    # Count syllables (simplified approach)
    def count_syllables(word):
        word = word.lower()
        if len(word) <= 3:
            return 1
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for i in range(1, len(word)):
            if word[i] in vowels and word[i-1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count = 1
        return count
    
    syllable_count = sum(count_syllables(word.strip(".,!?;:\"'()[]{}")) for word in words)
    
    # Calculate Flesch-Kincaid Grade Level (simplified)
    if word_count > 0:
        fk_grade = 0.39 * (word_count) + 11.8 * (syllable_count / word_count) - 15.59
    else:
        fk_grade = 0
    
    return fk_grade


def get_word_frequency(word: str) -> float:
    """
    Get the relative frequency of a word in English language
    Returns a float between 0 and 1, where higher values indicate more common words
    """
    # Common English words with approximate relative frequencies
    common_words = {
        "the": 0.95,
        "be": 0.94,
        "to": 0.93,
        "of": 0.92,
        "and": 0.91,
        "a": 0.90,
        "in": 0.89,
        "that": 0.88,
        "have": 0.87,
        "I": 0.86,
        "it": 0.85,
        "for": 0.84,
        "not": 0.83,
        "on": 0.82,
        "with": 0.81,
        "he": 0.80,
        "as": 0.79,
        "you": 0.78,
        "do": 0.77,
        "at": 0.76,
        "this": 0.75,
        "but": 0.74,
        "his": 0.73,
        "by": 0.72,
        "from": 0.71,
        "they": 0.70,
        "we": 0.69,
        "say": 0.68,
        "her": 0.67,
        "she": 0.66,
        "or": 0.65,
        "an": 0.64,
        "will": 0.63,
        "my": 0.62,
        "one": 0.61,
        "all": 0.60,
        "would": 0.59,
        "there": 0.58,
        "their": 0.57,
        "what": 0.56,
        "so": 0.55,
        "up": 0.54,
        "out": 0.53,
        "if": 0.52,
        "about": 0.51,
        "who": 0.50,
        "get": 0.49,
        "which": 0.48,
        "go": 0.47,
        "me": 0.46
    }
    
    # Return the frequency if the word is in our dictionary
    word = word.lower()
    if word in common_words:
        return common_words[word]
    
    # For words not in our dictionary, estimate based on length
    # Shorter words tend to be more common
    if len(word) <= 3:
        return 0.3
    elif len(word) <= 5:
        return 0.2
    elif len(word) <= 8:
        return 0.1
    else:
        return 0.05