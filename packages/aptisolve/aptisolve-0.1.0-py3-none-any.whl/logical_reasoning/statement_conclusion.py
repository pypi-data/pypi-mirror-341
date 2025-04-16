from typing import List, Dict, Union
import random

def analyze_statement_conclusion(statement: str, conclusions: List[str]) -> Dict[str, Union[List[bool], List[str]]]:
    """Analyze statements and determine which conclusions follow"""
    steps = [
        "Method to solve Statement and Conclusion problems:",
        "1. Understand the facts given in the statement",
        "2. Identify explicit and implicit information",
        "3. For each conclusion, check if it directly follows from the statement",
        "4. A conclusion follows only if it can be directly derived from the statement",
        "",
        f"Given statement: {statement}",
        "",
        "Given conclusions:"
    ]
    
    # Add conclusions
    for i, conclusion in enumerate(conclusions):
        steps.append(f"Conclusion {i+1}: {conclusion}")
    
    steps.append("")
    steps.append("Analysis:")
    
    # This is a placeholder for the actual analysis logic
    # In a real implementation, we would parse the statement and conclusions
    # and apply logical rules to determine which conclusions follow
    
    steps.append("Step 1: Identify key facts in the statement")
    steps.append("[Key facts would be listed here]")
    steps.append("")
    steps.append("Step 2: Analyze each conclusion")
    
    # Placeholder analysis for each conclusion
    conclusion_follows = [False] * len(conclusions)  # Placeholder
    
    for i, conclusion in enumerate(conclusions):
        steps.append(f"Conclusion {i+1}: {conclusion}")
        steps.append(f"  → [Analysis would be here]")
        steps.append(f"  → This conclusion {'follows' if conclusion_follows[i] else 'does not follow'}")
        steps.append("")
    
    steps.append("Final Answer: Conclusions that follow: [list of conclusions]")
    
    return {
        "follows": conclusion_follows,
        "steps": steps,
        "practice_tip": "Focus only on what can be directly inferred from the statement, avoiding assumptions."
    }

def generate_statement_conclusion_question(difficulty: str = "medium") -> Dict[str, Union[str, List[str], List[bool]]]:
    """Generate a statement and conclusion question with varying difficulty"""
    # Define templates for different difficulty levels
    templates = {
        "easy": [
            {
                "statement": "All fruits are sweet. All sweet things are tasty.",
                "conclusions": [
                    "All fruits are tasty",
                    "Some tasty things are fruits"
                ],
                "follows": [True, True],
                "explanation": "Conclusion 1 follows because if all fruits are sweet and all sweet things are tasty, then all fruits are tasty. Conclusion 2 follows because if all fruits are tasty, then some tasty things are fruits."
            }
        ],
        "medium": [
            {
                "statement": "Some books are interesting. All interesting things are educational.",
                "conclusions": [
                    "Some books are educational",
                    "All educational things are books",
                    "Some educational things are books"
                ],
                "follows": [True, False, True],
                "explanation": "Conclusion 1 follows because if some books are interesting and all interesting things are educational, then some books are educational. Conclusion 2 does not follow because the statement doesn't tell us that all educational things are books. Conclusion 3 follows because if some books are educational, then some educational things are books."
            }
        ],
        "hard": [
            {
                "statement": "No intelligent person is superstitious. Some educated people are superstitious.",
                "conclusions": [
                    "Some educated people are not intelligent",
                    "No educated person is intelligent",
                    "Some intelligent people are educated"
                ],
                "follows": [True, False, False],
                "explanation": "Conclusion 1 follows because if some educated people are superstitious and no intelligent person is superstitious, then those educated people who are superstitious cannot be intelligent. Conclusion 2 does not follow because the statement doesn't tell us that all educated people are superstitious. Conclusion 3 does not follow because the statement doesn't provide any information about whether any intelligent people are educated."
            }
        ]
    }
    
    # Select a template based on difficulty
    selected_template = random.choice(templates.get(difficulty, templates["medium"]))
    
    # Create question
    question = f"Statement: {selected_template['statement']}\n\nWhich of the following conclusions logically follow from the statement?"
    
    # Generate options
    options = []
    for i, (conclusion, follows) in enumerate(zip(selected_template["conclusions"], selected_template["follows"])):
        options.append(f"Conclusion {i+1}: {conclusion}")
    
    # Determine correct answer
    correct_indices = [i+1 for i, follows in enumerate(selected_template["follows"]) if follows]
    correct_answer = ", ".join(map(str, correct_indices))
    
    # Generate answer choices
    answer_choices = []
    if len(correct_indices) == 0:
        answer_choices.append("None of the conclusions follow")
    else:
        answer_choices.append(f"Only conclusion {correct_answer} follows")
    
    # Add some wrong choices
    all_indices = list(range(1, len(selected_template["conclusions"]) + 1))
    wrong_combinations = []
    
    # Generate wrong combinations
    for i in range(1, len(all_indices) + 1):
        for j in range(i+1, len(all_indices) + 1):
            if [i, j] != correct_indices and [j, i] != correct_indices:
                wrong_combinations.append(f"Only conclusions {i} and {j} follow")
    
    # Add "All conclusions follow" if that's not the correct answer
    if len(correct_indices) != len(selected_template["conclusions"]):
        wrong_combinations.append("All conclusions follow")
    
    # Select random wrong combinations
    random.shuffle(wrong_combinations)
    answer_choices.extend(wrong_combinations[:3])
    
    # Ensure we have exactly 4 choices
    while len(answer_choices) < 4:
        answer_choices.append(f"Only conclusion {random.randint(1, len(selected_template['conclusions']))} follows")
    
    answer_choices = answer_choices[:4]  # Limit to 4 options
    random.shuffle(answer_choices)
    
    # Find index of correct answer
    correct_option_text = f"Only conclusion {correct_answer} follows" if correct_indices else "None of the conclusions follow"
    correct_index = answer_choices.index(correct_option_text)
    
    return {
        "statement": selected_template["statement"],
        "conclusions": selected_template["conclusions"],
        "question": question,
        "options": answer_choices,
        "correct_answer": correct_option_text,
        "correct_option": chr(65 + correct_index),  # A, B, C, D
        "explanation": selected_template["explanation"],
        "difficulty": difficulty
    }