from typing import List, Dict, Union
import math
from fractions import Fraction

def calculate_probability(favorable_outcomes: int, total_outcomes: int) -> Dict[str, Union[float, List[str]]]:
    """Calculate probability with detailed steps"""
    if total_outcomes <= 0:
        return {
            "answer": "Error: Total outcomes must be positive",
            "steps": ["Error: Total outcomes must be positive"],
            "formula": "P(event) = Number of favorable outcomes / Total number of possible outcomes",
            "practice_tip": "Total outcomes must be a positive integer."
        }
    
    if favorable_outcomes < 0 or favorable_outcomes > total_outcomes:
        return {
            "answer": "Error: Favorable outcomes must be between 0 and total outcomes",
            "steps": ["Error: Favorable outcomes must be between 0 and total outcomes"],
            "formula": "P(event) = Number of favorable outcomes / Total number of possible outcomes",
            "practice_tip": "Favorable outcomes cannot exceed total outcomes."
        }
    
    steps = [
        "Method to calculate probability:",
        "Formula: P(event) = Number of favorable outcomes / Total number of possible outcomes",
        "",
        f"Given values: Favorable outcomes = {favorable_outcomes}, Total outcomes = {total_outcomes}",
        "",
        "Step-by-step calculation:"
    ]
    
    # Calculate probability
    probability = favorable_outcomes / total_outcomes
    
    # Express as a fraction in lowest terms
    fraction = Fraction(favorable_outcomes, total_outcomes)
    
    steps.append(f"P(event) = {favorable_outcomes} / {total_outcomes}")
    steps.append(f"P(event) = {probability}")
    
    if fraction.numerator != favorable_outcomes or fraction.denominator != total_outcomes:
        steps.append(f"P(event) = {fraction.numerator} / {fraction.denominator} (simplified fraction)")
    
    steps.append(f"P(event) = {probability:.4f} (decimal)")
    steps.append(f"P(event) = {probability * 100:.2f}% (percentage)")
    steps.append("")
    steps.append(f"Final Answer: P(event) = {probability:.4f} or {fraction.numerator}/{fraction.denominator}")
    
    return {
        "answer": probability,
        "fraction": f"{fraction.numerator}/{fraction.denominator}",
        "percentage": f"{probability * 100:.2f}%",
        "steps": steps,
        "formula": "P(event) = Number of favorable outcomes / Total number of possible outcomes",
        "practice_tip": "Express probability as a fraction in lowest terms, decimal, or percentage."
    }

def calculate_compound_probability(prob_a: float, prob_b: float, operation: str = "and") -> Dict[str, Union[float, List[str]]]:
    """Calculate compound probability (AND, OR) with detailed steps"""
    if not (0 <= prob_a <= 1 and 0 <= prob_b <= 1):
        return {
            "answer": "Error: Probabilities must be between 0 and 1",
            "steps": ["Error: Probabilities must be between 0 and 1"],
            "formula": "P(A and B) = P(A) × P(B) (for independent events)\nP(A or B) = P(A) + P(B) - P(A and B)",
            "practice_tip": "Probability values must be between 0 and 1."
        }
    
    steps = [
        "Method to calculate compound probability:",
        f"Given values: P(A) = {prob_a}, P(B) = {prob_b}",
        "",
        "Step-by-step calculation:"
    ]
    
    if operation.lower() == "and":
        # Calculate P(A and B) for independent events
        result = prob_a * prob_b
        
        steps.append("For independent events:")
        steps.append("Formula: P(A and B) = P(A) × P(B)")
        steps.append(f"P(A and B) = {prob_a} × {prob_b}")
        steps.append(f"P(A and B) = {result}")
        steps.append("")
        steps.append(f"Final Answer: P(A and B) = {result:.4f}")
        
        formula = "P(A and B) = P(A) × P(B) (for independent events)"
        practice_tip = "For dependent events, use P(A and B) = P(A) × P(B|A)."
        
    elif operation.lower() == "or":
        # Calculate P(A or B)
        p_a_and_b = prob_a * prob_b  # Assuming independence
        result = prob_a + prob_b - p_a_and_b
        
        steps.append("Formula: P(A or B) = P(A) + P(B) - P(A and B)")
        steps.append(f"P(A and B) = P(A) × P(B) = {prob_a} × {prob_b} = {p_a_and_b} (assuming independence)")
        steps.append(f"P(A or B) = {prob_a} + {prob_b} - {p_a_and_b}")
        steps.append(f"P(A or B) = {result}")
        steps.append("")
        steps.append(f"Final Answer: P(A or B) = {result:.4f}")
        
        formula = "P(A or B) = P(A) + P(B) - P(A and B)"
        practice_tip = "For mutually exclusive events, P(A or B) = P(A) + P(B) since P(A and B) = 0."
        
    else:
        return {
            "answer": "Error: Operation must be 'and' or 'or'",
            "steps": ["Error: Operation must be 'and' or 'or'"],
            "formula": "P(A and B) = P(A) × P(B) (for independent events)\nP(A or B) = P(A) + P(B) - P(A and B)",
            "practice_tip": "Specify 'and' for intersection or 'or' for union of events."
        }
    
    return {
        "answer": result,
        "steps": steps,
        "formula": formula,
        "practice_tip": practice_tip
    }

def calculate_conditional_probability(prob_a: float, prob_b_given_a: float) -> Dict[str, Union[float, List[str]]]:
    """Calculate conditional probability with detailed steps"""
    if not (0 <= prob_a <= 1 and 0 <= prob_b_given_a <= 1):
        return {
            "answer": "Error: Probabilities must be between 0 and 1",
            "steps": ["Error: Probabilities must be between 0 and 1"],
            "formula": "P(A and B) = P(A) × P(B|A)",
            "practice_tip": "Probability values must be between 0 and 1."
        }
    
    steps = [
        "Method to calculate joint probability using conditional probability:",
        "Formula: P(A and B) = P(A) × P(B|A)",
        "",
        f"Given values: P(A) = {prob_a}, P(B|A) = {prob_b_given_a}",
        "",
        "Step-by-step calculation:"
    ]
    
    # Calculate P(A and B)
    joint_prob = prob_a * prob_b_given_a
    
    steps.append(f"P(A and B) = P(A) × P(B|A)")
    steps.append(f"P(A and B) = {prob_a} × {prob_b_given_a}")
    steps.append(f"P(A and B) = {joint_prob}")
    steps.append("")
    steps.append(f"Final Answer: P(A and B) = {joint_prob:.4f}")
    
    return {
        "answer": joint_prob,
        "steps": steps,
        "formula": "P(A and B) = P(A) × P(B|A)",
        "practice_tip": "Conditional probability helps calculate joint probability when events are dependent."
    }

def calculate_bayes_theorem(prob_a: float, prob_b_given_a: float, prob_b_given_not_a: float) -> Dict[str, Union[float, List[str]]]:
    """Calculate probability using Bayes' Theorem with detailed steps"""
    if not (0 <= prob_a <= 1 and 0 <= prob_b_given_a <= 1 and 0 <= prob_b_given_not_a <= 1):
        return {
            "answer": "Error: Probabilities must be between 0 and 1",
            "steps": ["Error: Probabilities must be between 0 and 1"],
            "formula": "P(A|B) = [P(B|A) × P(A)] / [P(B|A) × P(A) + P(B|not A) × P(not A)]",
            "practice_tip": "Probability values must be between 0 and 1."
        }
    
    steps = [
        "Method to calculate probability using Bayes' Theorem:",
        "Formula: P(A|B) = [P(B|A) × P(A)] / [P(B|A) × P(A) + P(B|not A) × P(not A)]",
        "",
        f"Given values: P(A) = {prob_a}, P(B|A) = {prob_b_given_a}, P(B|not A) = {prob_b_given_not_a}",
        "",
        "Step-by-step calculation:"
    ]
    
    # Calculate P(not A)
    prob_not_a = 1 - prob_a
    steps.append(f"Step 1: Calculate P(not A)")
    steps.append(f"P(not A) = 1 - P(A) = 1 - {prob_a} = {prob_not_a}")
    steps.append("")
    
    # Calculate P(B|A) × P(A)
    numerator = prob_b_given_a * prob_a
    steps.append(f"Step 2: Calculate P(B|A) × P(A)")
    steps.append(f"P(B|A) × P(A) = {prob_b_given_a} × {prob_a} = {numerator}")
    steps.append("")
    
    # Calculate P(B|not A) × P(not A)
    term2 = prob_b_given_not_a * prob_not_a
    steps.append(f"Step 3: Calculate P(B|not A) × P(not A)")
    steps.append(f"P(B|not A) × P(not A) = {prob_b_given_not_a} × {prob_not_a} = {term2}")
    steps.append("")
    
    # Calculate denominator
    denominator = numerator + term2
    steps.append(f"Step 4: Calculate denominator = P(B|A) × P(A) + P(B|not A) × P(not A)")
    steps.append(f"Denominator = {numerator} + {term2} = {denominator}")
    steps.append("")
    
    # Calculate P(A|B)
    if denominator == 0:
        return {
            "answer": "Error: Denominator is zero",
            "steps": ["Error: Denominator is zero, cannot calculate P(A|B)"],
            "formula": "P(A|B) = [P(B|A) × P(A)] / [P(B|A) × P(A) + P(B|not A) × P(not A)]",
            "practice_tip": "Ensure that P(B) is not zero."
        }
    
    result = numerator / denominator
    steps.append(f"Step 5: Calculate P(A|B) = [P(B|A) × P(A)] / denominator")
    steps.append(f"P(A|B) = {numerator} / {denominator} = {result}")
    steps.append("")
    steps.append(f"Final Answer: P(A|B) = {result:.4f}")
    
    return {
        "answer": result,
        "steps": steps,
        "formula": "P(A|B) = [P(B|A) × P(A)] / [P(B|A) × P(A) + P(B|not A) × P(not A)]",
        "practice_tip": "Bayes' Theorem is useful for updating probabilities based on new evidence."
    }