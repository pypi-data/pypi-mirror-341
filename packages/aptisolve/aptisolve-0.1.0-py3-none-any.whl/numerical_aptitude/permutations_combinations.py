from typing import List, Dict, Union
import math

def calculate_factorial(n: int) -> Dict[str, Union[int, List[str]]]:
    """Calculate factorial with detailed steps"""
    if n < 0:
        return {
            "answer": "Error: Factorial is not defined for negative numbers",
            "steps": ["Error: Factorial is not defined for negative numbers"],
            "formula": "n! = n × (n-1) × (n-2) × ... × 2 × 1",
            "practice_tip": "Factorial is only defined for non-negative integers."
        }
    
    result = 1
    steps = [
        "Method to calculate factorial:",
        "Formula: n! = n × (n-1) × (n-2) × ... × 2 × 1",
        "",
        f"Given number: {n}",
        "",
        "Step-by-step calculation:"
    ]
    
    if n == 0 or n == 1:
        steps.append(f"{n}! = 1 (by definition)")
    else:
        calculation = f"{n}! = "
        factors = []
        
        for i in range(n, 0, -1):
            factors.append(str(i))
            result *= i
        
        calculation += " × ".join(factors)
        calculation += f" = {result}"
        steps.append(calculation)
    
    steps.append("")
    steps.append(f"Final Answer: {n}! = {result}")
    
    return {
        "answer": result,
        "steps": steps,
        "formula": "n! = n × (n-1) × (n-2) × ... × 2 × 1",
        "practice_tip": "For large numbers, use the factorial function in a calculator or programming language."
    }

def calculate_permutation(n: int, r: int) -> Dict[str, Union[int, List[str]]]:
    """Calculate permutation (nPr) with detailed steps"""
    if n < 0 or r < 0:
        return {
            "answer": "Error: Permutation is not defined for negative numbers",
            "steps": ["Error: Permutation is not defined for negative numbers"],
            "formula": "P(n,r) = n! / (n-r)!",
            "practice_tip": "Both n and r must be non-negative integers."
        }
    
    if r > n:
        return {
            "answer": "Error: r cannot be greater than n in permutation",
            "steps": ["Error: r cannot be greater than n in permutation"],
            "formula": "P(n,r) = n! / (n-r)!",
            "practice_tip": "In permutation, you cannot select more items (r) than available (n)."
        }
    
    steps = [
        "Method to calculate permutation:",
        "Formula: P(n,r) = n! / (n-r)!",
        "",
        f"Given values: n = {n}, r = {r}",
        "",
        "Step-by-step calculation:"
    ]
    
    # Calculate n!
    n_factorial = math.factorial(n)
    steps.append(f"Step 1: Calculate n!")
    steps.append(f"{n}! = {n_factorial}")
    steps.append("")
    
    # Calculate (n-r)!
    n_minus_r = n - r
    n_minus_r_factorial = math.factorial(n_minus_r)
    steps.append(f"Step 2: Calculate (n-r)!")
    steps.append(f"({n} - {r})! = {n_minus_r}! = {n_minus_r_factorial}")
    steps.append("")
    
    # Calculate permutation
    permutation = n_factorial // n_minus_r_factorial
    steps.append(f"Step 3: Calculate P(n,r) = n! / (n-r)!")
    steps.append(f"P({n},{r}) = {n}! / ({n}-{r})!")
    steps.append(f"P({n},{r}) = {n_factorial} / {n_minus_r_factorial}")
    steps.append(f"P({n},{r}) = {permutation}")
    steps.append("")
    steps.append(f"Final Answer: P({n},{r}) = {permutation}")
    
    return {
        "answer": permutation,
        "steps": steps,
        "formula": "P(n,r) = n! / (n-r)!",
        "practice_tip": "Permutation counts arrangements where order matters."
    }

def calculate_combination(n: int, r: int) -> Dict[str, Union[int, List[str]]]:
    """Calculate combination (nCr) with detailed steps"""
    if n < 0 or r < 0:
        return {
            "answer": "Error: Combination is not defined for negative numbers",
            "steps": ["Error: Combination is not defined for negative numbers"],
            "formula": "C(n,r) = n! / (r! × (n-r)!)",
            "practice_tip": "Both n and r must be non-negative integers."
        }
    
    if r > n:
        return {
            "answer": "Error: r cannot be greater than n in combination",
            "steps": ["Error: r cannot be greater than n in combination"],
            "formula": "C(n,r) = n! / (r! × (n-r)!)",
            "practice_tip": "In combination, you cannot select more items (r) than available (n)."
        }
    
    steps = [
        "Method to calculate combination:",
        "Formula: C(n,r) = n! / (r! × (n-r)!)",
        "",
        f"Given values: n = {n}, r = {r}",
        "",
        "Step-by-step calculation:"
    ]
    
    # Calculate n!
    n_factorial = math.factorial(n)
    steps.append(f"Step 1: Calculate n!")
    steps.append(f"{n}! = {n_factorial}")
    steps.append("")
    
    # Calculate r!
    r_factorial = math.factorial(r)
    steps.append(f"Step 2: Calculate r!")
    steps.append(f"{r}! = {r_factorial}")
    steps.append("")
    
    # Calculate (n-r)!
    n_minus_r = n - r
    n_minus_r_factorial = math.factorial(n_minus_r)
    steps.append(f"Step 3: Calculate (n-r)!")
    steps.append(f"({n} - {r})! = {n_minus_r}! = {n_minus_r_factorial}")
    steps.append("")
    
    # Calculate combination
    combination = n_factorial // (r_factorial * n_minus_r_factorial)
    steps.append(f"Step 4: Calculate C(n,r) = n! / (r! × (n-r)!)")
    steps.append(f"C({n},{r}) = {n}! / ({r}! × ({n}-{r})!)")
    steps.append(f"C({n},{r}) = {n_factorial} / ({r_factorial} × {n_minus_r_factorial})")
    steps.append(f"C({n},{r}) = {n_factorial} / {r_factorial * n_minus_r_factorial}")
    steps.append(f"C({n},{r}) = {combination}")
    steps.append("")
    steps.append(f"Final Answer: C({n},{r}) = {combination}")
    
    return {
        "answer": combination,
        "steps": steps,
        "formula": "C(n,r) = n! / (r! × (n-r)!)",
        "practice_tip": "Combination counts selections where order doesn't matter."
    }

def permutation_with_repetition(n: int, r: int) -> Dict[str, Union[int, List[str]]]:
    """Calculate permutation with repetition allowed with detailed steps"""
    if n < 0 or r < 0:
        return {
            "answer": "Error: Values must be non-negative",
            "steps": ["Error: Values must be non-negative"],
            "formula": "P(n,r) with repetition = n^r",
            "practice_tip": "Both n and r must be non-negative integers."
        }
    
    steps = [
        "Method to calculate permutation with repetition:",
        "Formula: P(n,r) with repetition = n^r",
        "",
        f"Given values: n = {n}, r = {r}",
        "",
        "Step-by-step calculation:"
    ]
    
    # Calculate permutation with repetition
    permutation = n ** r
    steps.append(f"P({n},{r}) with repetition = {n}^{r}")
    steps.append(f"P({n},{r}) with repetition = {permutation}")
    steps.append("")
    steps.append(f"Final Answer: P({n},{r}) with repetition = {permutation}")
    
    return {
        "answer": permutation,
        "steps": steps,
        "formula": "P(n,r) with repetition = n^r",
        "practice_tip": "When repetition is allowed, each position has n choices."
    }

def combination_with_repetition(n: int, r: int) -> Dict[str, Union[int, List[str]]]:
    """Calculate combination with repetition allowed with detailed steps"""
    if n < 0 or r < 0:
        return {
            "answer": "Error: Values must be non-negative",
            "steps": ["Error: Values must be non-negative"],
            "formula": "C(n,r) with repetition = C(n+r-1,r)",
            "practice_tip": "Both n and r must be non-negative integers."
        }
    
    steps = [
        "Method to calculate combination with repetition:",
        "Formula: C(n,r) with repetition = C(n+r-1,r) = (n+r-1)! / (r! × (n-1)!)",
        "",
        f"Given values: n = {n}, r = {r}",
        "",
        "Step-by-step calculation:"
    ]
    
    # Calculate (n+r-1)!
    n_plus_r_minus_1 = n + r - 1
    n_plus_r_minus_1_factorial = math.factorial(n_plus_r_minus_1)
    steps.append(f"Step 1: Calculate (n+r-1)!")
    steps.append(f"({n}+{r}-1)! = {n_plus_r_minus_1}! = {n_plus_r_minus_1_factorial}")
    steps.append("")
    
    # Calculate r!
    r_factorial = math.factorial(r)
    steps.append(f"Step 2: Calculate r!")
    steps.append(f"{r}! = {r_factorial}")
    steps.append("")
    
    # Calculate (n-1)!
    n_minus_1 = n - 1
    n_minus_1_factorial = math.factorial(n_minus_1)
    steps.append(f"Step 3: Calculate (n-1)!")
    steps.append(f"({n}-1)! = {n_minus_1}! = {n_minus_1_factorial}")
    steps.append("")
    
    # Calculate combination with repetition
    combination = n_plus_r_minus_1_factorial // (r_factorial * n_minus_1_factorial)
    steps.append(f"Step 4: Calculate C(n,r) with repetition = (n+r-1)! / (r! × (n-1)!)")
    steps.append(f"C({n},{r}) with repetition = ({n}+{r}-1)! / ({r}! × ({n}-1)!)")
    steps.append(f"C({n},{r}) with repetition = {n_plus_r_minus_1}! / ({r}! × {n_minus_1}!)")
    steps.append(f"C({n},{r}) with repetition = {n_plus_r_minus_1_factorial} / ({r_factorial} × {n_minus_1_factorial})")
    steps.append(f"C({n},{r}) with repetition = {n_plus_r_minus_1_factorial} / {r_factorial * n_minus_1_factorial}")
    steps.append(f"C({n},{r}) with repetition = {combination}")
    steps.append("")
    steps.append(f"Final Answer: C({n},{r}) with repetition = {combination}")
    
    return {
        "answer": combination,
        "steps": steps,
        "formula": "C(n,r) with repetition = (n+r-1)! / (r! × (n-1)!)",
        "practice_tip": "This is also known as 'stars and bars' method in combinatorics."
    }