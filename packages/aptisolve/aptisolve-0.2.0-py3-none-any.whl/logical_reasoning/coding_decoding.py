from typing import List, Dict, Union
import random
import string

def decode_message(coded_message: str, coding_rule: str) -> Dict[str, Union[str, List[str]]]:
    """Decode a message based on the given coding rule with detailed steps"""
    steps = [
        "Method to solve Coding-Decoding problems:",
        "1. Understand the coding pattern/rule",
        "2. Apply the rule in reverse to decode",
        "3. Verify the decoded message makes sense",
        "",
        f"Coded message: {coded_message}",
        f"Coding rule: {coding_rule}",
        "",
        "Step-by-step decoding:"
    ]
    
    decoded_message = ""
    
    # Simple shift cipher (Caesar cipher)
    if "shift" in coding_rule.lower() or "caesar" in coding_rule.lower():
        # Extract shift value
        shift_value = 1  # Default
        for word in coding_rule.split():
            if word.isdigit():
                shift_value = int(word)
                break
        
        steps.append(f"This is a shift cipher with shift value {shift_value}")
        steps.append("For each letter, shift back in the alphabet by the shift value")
        steps.append("")
        
        # Process each character
        char_steps = []
        for char in coded_message:
            if char.isalpha():
                # Determine if uppercase or lowercase
                is_upper = char.isupper()
                # Convert to 0-25 range
                char_code = ord(char.lower()) - ord('a')
                # Shift backward
                new_code = (char_code - shift_value) % 26
                # Convert back to letter
                new_char = chr(new_code + ord('a'))
                # Restore case
                if is_upper:
                    new_char = new_char.upper()
                
                char_steps.append(f"{char} → shift back by {shift_value} → {new_char}")
                decoded_message += new_char
            else:
                decoded_message += char
                char_steps.append(f"{char} → (not a letter, unchanged)")
        
        steps.extend(char_steps)
    
    # Reverse coding
    elif "reverse" in coding_rule.lower():
        steps.append("This is a reverse coding")
        steps.append("Simply reverse the order of characters")
        
        decoded_message = coded_message[::-1]
        steps.append(f"{coded_message} → {decoded_message}")
    
    # Number-to-letter coding (1=A, 2=B, etc.)
    elif "number" in coding_rule.lower() and "letter" in coding_rule.lower():
        steps.append("This is a number-to-letter coding")
        steps.append("Convert each number to its corresponding letter (1=A, 2=B, etc.)")
        steps.append("")
        
        # Process each number
        char_steps = []
        numbers = coded_message.split()
        for num in numbers:
            if num.isdigit():
                num_val = int(num)
                if 1 <= num_val <= 26:
                    letter = chr(num_val + ord('a') - 1)
                    char_steps.append(f"{num} → {letter}")
                    decoded_message += letter
                else:
                    decoded_message += " "
                    char_steps.append(f"{num} → (out of range, replaced with space)")
            else:
                decoded_message += num
                char_steps.append(f"{num} → (not a number, unchanged)")
        
        steps.extend(char_steps)
    
    # Substitution cipher (each letter is replaced by another)
    else:
        steps.append("This appears to be a substitution cipher")
        steps.append("Each letter is replaced according to a specific pattern")
        steps.append("Without the exact substitution rule, we can only make educated guesses")
        
        decoded_message = "Cannot decode without specific substitution rule"
    
    steps.append("")
    steps.append(f"Decoded message: {decoded_message}")
    
    return {
        "decoded_message": decoded_message,
        "steps": steps,
        "practice_tip": "For shift ciphers, try different shift values if the decoded message doesn't make sense."
    }

def generate_coding_question(difficulty: str = "medium") -> Dict[str, Union[str, List[str], str]]:
    """Generate a coding-decoding question with varying difficulty"""
    # Define templates for different difficulty levels
    templates = {
        "easy": [
            {
                "rule": "Shift cipher with shift value 1",
                "original": "HELLO WORLD",
                "coded": "IFMMP XPSME",
                "question": "If HELLO WORLD is coded as IFMMP XPSME, then how is APPLE coded?",
                "answer": "BQQMF",
                "explanation": "This is a shift cipher where each letter is replaced by the next letter in the alphabet. A→B, P→Q, P→Q, L→M, E→F."
            }
        ],
        "medium": [
            {
                "rule": "Each letter is replaced by a letter that is 3 positions ahead in the alphabet",
                "original": "LOGIC",
                "coded": "ORJLF",
                "question": "If LOGIC is coded as ORJLF, then how is PUZZLE coded?",
                "answer": "SXCCOH",
                "explanation": "This is a shift cipher with shift value 3. P→S, U→X, Z→C, Z→C, L→O, E→H."
            }
        ],
        "hard": [
            {
                "rule": "Each letter is replaced by a letter that is at the same position from the opposite end of the alphabet (A→Z, B→Y, etc.)",
                "original": "CIPHER",
                "coded": "XRKSVI",
                "question": "If CIPHER is coded as XRKSVI, then how is DECODE coded?",
                "answer": "WVXLWV",
                "explanation": "This is an Atbash cipher where each letter is replaced by the letter at the same position from the opposite end. D→W, E→V, C→X, O→L, D→W, E→V."
            }
        ]
    }
    
    # Select a template based on difficulty
    selected_template = random.choice(templates.get(difficulty, templates["medium"]))
    
    # Generate options (including the correct answer)
    correct_answer = selected_template["answer"]
    
    # Generate wrong options based on the type of coding
    wrong_options = []
    
    if "shift" in selected_template["rule"].lower():
        # For shift ciphers, use different shift values
        original_word = selected_template["question"].split("then how is ")[1].split()[0].strip("?")
        shift_values = [1, 2, 3, 4, 5]
        correct_shift = None
        
        # Determine the correct shift
        for shift in shift_values:
            shifted = ''.join([chr((ord(c.upper()) - ord('A') + shift) % 26 + ord('A')) if c.isalpha() else c for c in original_word])
            if shifted == correct_answer:
                correct_shift = shift
                break
        
        # Generate wrong options with different shifts
        for _ in range(3):
            wrong_shift = random.choice([s for s in shift_values if s != correct_shift])
            wrong_option = ''.join([chr((ord(c.upper()) - ord('A') + wrong_shift) % 26 + ord('A')) if c.isalpha() else c for c in original_word])
            if wrong_option != correct_answer and wrong_option not in wrong_options:
                wrong_options.append(wrong_option)
    
    else:
        # For other types, generate random variations
        for _ in range(3):
            wrong_chars = ''.join(random.choices(string.ascii_uppercase, k=len(correct_answer)))
            if wrong_chars != correct_answer and wrong_chars not in wrong_options:
                wrong_options.append(wrong_chars)
    
    # Ensure we have exactly 3 wrong options
    while len(wrong_options) < 3:
        wrong_chars = ''.join(random.choices(string.ascii_uppercase, k=len(correct_answer)))
        if wrong_chars != correct_answer and wrong_chars not in wrong_options:
            wrong_options.append(wrong_chars)
    
    wrong_options = wrong_options[:3]  # Limit to 3 options
    
    all_options = wrong_options + [correct_answer]
    random.shuffle(all_options)
    
    # Find index of correct answer
    correct_index = all_options.index(correct_answer)
    
    return {
        "original": selected_template["original"],
        "coded": selected_template["coded"],
        "question": selected_template["question"],
        "options": all_options,
        "correct_answer": correct_answer,
        "correct_option": chr(65 + correct_index),  # A, B, C, D
        "explanation": selected_template["explanation"],
        "difficulty": difficulty,
        "rule": selected_template["rule"]
    }