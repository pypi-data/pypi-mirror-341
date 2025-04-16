from typing import List, Dict, Union

def calculate_simple_interest(principal: float, rate: float, time: float) -> Dict[str, Union[float, List[str]]]:
    """Calculate simple interest with detailed steps for practice"""
    interest = (principal * rate * time) / 100
    amount = principal + interest
    
    steps = [
        "Method to solve Simple Interest problems:",
        "Formula: SI = (P × R × T) ÷ 100",
        "",
        f"Given values:",
        f"→ Principal (P) = ${principal}",
        f"→ Rate (R) = {rate}%",
        f"→ Time (T) = {time} years",
        "",
        "Step 1: Multiply P, R, and T",
        f"→ {principal} × {rate} × {time}",
        f"→ {principal * rate * time}",
        "",
        "Step 2: Divide by 100",
        f"→ {principal * rate * time} ÷ 100",
        f"→ Interest = ${interest}",
        "",
        "Step 3: Calculate total amount",
        f"→ Amount = Principal + Interest",
        f"→ Amount = ${principal} + ${interest}",
        f"→ Amount = ${amount}",
        "",
        f"Final Answer: ${round(amount, 2)}"
    ]
    
    return {
        "answer": round(amount, 2),
        "interest": round(interest, 2),
        "steps": steps,
        "formula": "Simple Interest = (Principal × Rate × Time) ÷ 100",
        "practice_tip": "Remember to divide by 100 since rate is in percentage, and add interest to principal for total amount"
    }
