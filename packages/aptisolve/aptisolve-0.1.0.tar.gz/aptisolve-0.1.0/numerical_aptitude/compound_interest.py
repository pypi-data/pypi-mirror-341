from typing import List, Dict, Union

def calculate_compound_interest(principal: float, rate: float, time: float, n: int = 1) -> Dict[str, Union[float, List[str]]]:
    """Calculate compound interest with detailed steps for practice"""
    rate_decimal = rate / 100
    amount = principal * (1 + rate_decimal/n)**(n*time)
    interest = amount - principal
    
    steps = [
        "Method to solve Compound Interest problems:",
        "Formula: A = P(1 + r/n)^(nt)",
        "",
        f"Given values:",
        f"→ Principal (P) = ${principal}",
        f"→ Rate (r) = {rate}%",
        f"→ Time (t) = {time} years",
        f"→ Compounds per year (n) = {n}",
        "",
        "Step 1: Convert rate to decimal",
        f"→ {rate}% = {rate}/100 = {rate_decimal}",
        "",
        "Step 2: Calculate r/n",
        f"→ {rate_decimal}/{n} = {rate_decimal/n}",
        "",
        "Step 3: Calculate nt",
        f"→ {n} × {time} = {n*time}",
        "",
        "Step 4: Apply the formula",
        f"→ A = {principal} × (1 + {rate_decimal/n})^{n*time}",
        f"→ Amount = ${round(amount, 2)}",
        "",
        "Step 5: Calculate interest",
        f"→ Interest = Amount - Principal",
        f"→ Interest = ${round(amount, 2)} - ${principal}",
        f"→ Interest = ${round(interest, 2)}",
        "",
        f"Final Answer: ${round(amount, 2)}"
    ]
    
    return {
        "answer": round(amount, 2),
        "interest": round(interest, 2),
        "steps": steps,
        "formula": "A = P(1 + r/n)^(nt)",
        "practice_tip": "Take special care with the exponent calculation, and remember to convert rate to decimal form"
    }