from typing import List, Dict, Union
import random

# Define relationship types and their descriptions
RELATIONSHIPS = {
    "father": "male parent",
    "mother": "female parent",
    "son": "male child",
    "daughter": "female child",
    "brother": "male sibling",
    "sister": "female sibling",
    "grandfather": "father's or mother's father",
    "grandmother": "father's or mother's mother",
    "grandson": "son's or daughter's son",
    "granddaughter": "son's or daughter's daughter",
    "uncle": "father's or mother's brother",
    "aunt": "father's or mother's sister",
    "nephew": "brother's or sister's son",
    "niece": "brother's or sister's daughter",
    "cousin": "uncle's or aunt's son or daughter",
    "husband": "male spouse",
    "wife": "female spouse"
}

def solve_blood_relation(statements: List[str], question: str) -> Dict[str, Union[str, List[str]]]:
    """Solve blood relation problems with detailed steps"""
    steps = [
        "Method to solve Blood Relation problems:",
        "1. Draw a family tree diagram",
        "2. Establish relationships one by one",
        "3. Use symbols (M for male, F for female)",
        "4. Trace the relationship path",
        "",
        "Given statements:"
    ]
    
    # Add each statement
    for i, statement in enumerate(statements):
        steps.append(f"Statement {i+1}: {statement}")
    
    steps.append("")
    steps.append(f"Question: {question}")
    steps.append("")
    steps.append("Analysis:")
    
    # This is a placeholder for the actual solving logic
    # In a real implementation, we would parse the statements and build a family tree
    
    steps.append("Step 1: Draw a family tree based on the given statements")
    steps.append("[Family tree diagram would be drawn here]")
    steps.append("")
    steps.append("Step 2: Trace the relationship path to answer the question")
    steps.append("[Relationship path would be traced here]")
    steps.append("")
    steps.append("Final Answer: [Relationship]")
    
    return {
        "answer": "Placeholder answer",
        "steps": steps,
        "practice_tip": "Always draw a family tree diagram to visualize relationships."
    }

def generate_relation_question(difficulty: str = "medium") -> Dict[str, Union[str, List[str], str]]:
    """Generate a blood relation question with varying difficulty"""
    # Define templates for different difficulty levels
    templates = {
        "easy": [
            {
                "statements": [
                    "A is the father of B",
                    "C is the mother of B"
                ],
                "question": "How is A related to C?",
                "answer": "husband",
                "explanation": "A is the father of B and C is the mother of B, so A is the husband of C."
            },
            {
                "statements": [
                    "P is the son of Q",
                    "Q is the daughter of R"
                ],
                "question": "How is R related to P?",
                "answer": "grandfather",
                "explanation": "P is the son of Q and Q is the daughter of R, so R is the grandfather of P."
            }
        ],
        "medium": [
            {
                "statements": [
                    "A is the brother of B",
                    "C is the daughter of B",
                    "D is the father of A"
                ],
                "question": "How is D related to C?",
                "answer": "grandfather",
                "explanation": "A is the brother of B, so B is A's sibling. C is the daughter of B. D is the father of A, which makes D the father of B as well. Therefore, D is the grandfather of C."
            },
            {
                "statements": [
                    "P is the wife of Q",
                    "R is the brother of P",
                    "S is the daughter of Q"
                ],
                "question": "How is R related to S?",
                "answer": "uncle",
                "explanation": "P is the wife of Q, and S is the daughter of Q, which means S is also the daughter of P. R is the brother of P, which makes R the uncle of S."
            }
        ],
        "hard": [
            {
                "statements": [
                    "A is the father of B",
                    "C is the daughter of D",
                    "E is the father of C",
                    "B and D are siblings",
                    "F is the wife of A"
                ],
                "question": "How is F related to C?",
                "answer": "aunt",
                "explanation": "A is the father of B. F is the wife of A, so F is the mother of B. B and D are siblings, which means they share the same parents. So, F is also the mother of D. C is the daughter of D, which makes F the grandmother of C. However, E is the father of C, not A. This means D is not the wife of A but the sister of B. Therefore, F is the aunt of C."
            }
        ]
    }
    
    # Select a template based on difficulty
    selected_template = random.choice(templates.get(difficulty, templates["medium"]))
    
    # Generate options (including the correct answer)
    correct_answer = selected_template["answer"]
    all_relationships = list(RELATIONSHIPS.keys())
    wrong_options = random.sample([r for r in all_relationships if r != correct_answer], 3)
    
    all_options = wrong_options + [correct_answer]
    random.shuffle(all_options)
    
    # Find index of correct answer
    correct_index = all_options.index(correct_answer)
    
    return {
        "statements": selected_template["statements"],
        "question": selected_template["question"],
        "options": all_options,
        "correct_answer": correct_answer,
        "correct_option": chr(65 + correct_index),  # A, B, C, D
        "explanation": selected_template["explanation"],
        "difficulty": difficulty
    }