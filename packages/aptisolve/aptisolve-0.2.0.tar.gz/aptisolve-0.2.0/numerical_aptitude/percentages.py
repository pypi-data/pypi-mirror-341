from typing import List, Dict, Union

def calculate_percentage(value: float, percentage: float) -> Dict[str, Union[float, List[str]]]:
    """Calculate percentage with detailed steps for practice"""
    result = (percentage / 100) * value
    
    steps = [
        "Method to solve Percentage problems:",
        "Formula: Percentage of a number = (Percentage ÷ 100) × Number",
        "",
        f"Given values:",
        f"→ Number = {value}",
        f"→ Percentage = {percentage}%",
        "",
        "Step 1: Convert percentage to decimal",
        f"→ {percentage} ÷ 100 = {percentage/100}",
        "",
        "Step 2: Multiply by the number",
        f"→ {percentage/100} × {value}",
        f"→ {result}",
        "",
        f"Final Answer: {round(result, 2)}"
    ]
    
    return {
        "answer": round(result, 2),
        "steps": steps,
        "formula": "Percentage = (Percentage ÷ 100) × Number",
        "practice_tip": "Always convert percentage to decimal first by dividing by 100, then multiply with the number"
    }


def calculate_increase_after_percentage(original_value, percentage):
    """
    Calculate the value after a percentage increase.
    
    Args:
        original_value (float): The original value
        percentage (float): The percentage increase
        
    Returns:
        dict: A dictionary containing the result and steps
    """
    steps = [
        f"Original value: {original_value}",
        f"Percentage increase: {percentage}%"
    ]
    
    increase = original_value * (percentage / 100)
    steps.append(f"Calculate the increase: {original_value} × ({percentage}/100) = {increase}")
    
    new_value = original_value + increase
    steps.append(f"Add the increase to the original value: {original_value} + {increase} = {new_value}")
    
    return {
        "answer": new_value,
        "increase": increase,
        "steps": steps
    }
