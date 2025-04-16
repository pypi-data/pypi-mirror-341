from typing import Dict, Union, List

def divide_in_ratio(value: float, ratio1: int, ratio2: int) -> Dict[str, Union[float, List[str]]]:
    steps = []
    steps.append(f"Dividing {value} in the ratio {ratio1}:{ratio2}")
    
    total_parts = ratio1 + ratio2
    steps.append(f"Step 1: Calculate the total number of parts")
    steps.append(f"Total parts = {ratio1} + {ratio2} = {total_parts}")
    
    value_per_part = value / total_parts
    steps.append(f"Step 2: Calculate the value of each part")
    steps.append(f"Value per part = {value} ÷ {total_parts} = {value_per_part}")
    
    first_share = value_per_part * ratio1
    second_share = value_per_part * ratio2
    
    steps.append(f"Step 3: Calculate the share for each ratio")
    steps.append(f"First share = {value_per_part} × {ratio1} = {first_share}")
    steps.append(f"Second share = {value_per_part} × {ratio2} = {second_share}")
    
    return {
        "first_share": first_share,
        "second_share": second_share,
        "steps": steps
    }

def calculate_ratio(num1: float, num2: float) -> Dict[str, Union[str, List[str]]]:
    steps = []
    steps.append(f"Finding the ratio between {num1} and {num2}")
    
    # Find the greatest common divisor (GCD)
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    # Convert to integers if they're whole numbers
    if num1.is_integer() and num2.is_integer():
        num1 = int(num1)
        num2 = int(num2)
        
        common_divisor = gcd(num1, num2)
        simplified_num1 = num1 // common_divisor
        simplified_num2 = num2 // common_divisor
        
        steps.append(f"Step 1: Find the greatest common divisor (GCD) of {num1} and {num2}")
        steps.append(f"GCD = {common_divisor}")
        
        steps.append(f"Step 2: Divide both numbers by the GCD")
        steps.append(f"{num1} ÷ {common_divisor} = {simplified_num1}")
        steps.append(f"{num2} ÷ {common_divisor} = {simplified_num2}")
        
        simplified_ratio = f"{simplified_num1}:{simplified_num2}"
    else:
        # For decimal numbers, find a common multiplier to convert to integers
        multiplier = 1
        while not (num1 * multiplier).is_integer() or not (num2 * multiplier).is_integer():
            multiplier *= 10
            
        int_num1 = int(num1 * multiplier)
        int_num2 = int(num2 * multiplier)
        
        steps.append(f"Step 1: Convert decimal numbers to integers by multiplying by {multiplier}")
        steps.append(f"{num1} × {multiplier} = {int_num1}")
        steps.append(f"{num2} × {multiplier} = {int_num2}")
        
        common_divisor = gcd(int_num1, int_num2)
        simplified_num1 = int_num1 // common_divisor
        simplified_num2 = int_num2 // common_divisor
        
        steps.append(f"Step 2: Find the greatest common divisor (GCD) of {int_num1} and {int_num2}")
        steps.append(f"GCD = {common_divisor}")
        
        steps.append(f"Step 3: Divide both numbers by the GCD")
        steps.append(f"{int_num1} ÷ {common_divisor} = {simplified_num1}")
        steps.append(f"{int_num2} ÷ {common_divisor} = {simplified_num2}")
        
        simplified_ratio = f"{simplified_num1}:{simplified_num2}"
    
    steps.append(f"The simplified ratio is {simplified_ratio}")
    
    return {
        "simplified_ratio": simplified_ratio,
        "steps": steps
    }

def solve_proportion(a: float, b: float, c: float) -> Dict[str, Union[float, List[str]]]:
    steps = []
    steps.append(f"Solving the proportion: {a}:{b} = {c}:x")
    
    steps.append(f"Step 1: Set up the proportion equation")
    steps.append(f"{a}/{b} = {c}/x")
    
    steps.append(f"Step 2: Cross multiply")
    steps.append(f"{a} × x = {b} × {c}")
    steps.append(f"{a}x = {b*c}")
    
    steps.append(f"Step 3: Solve for x")
    steps.append(f"x = ({b} × {c}) ÷ {a}")
    
    answer = (b * c) / a
    steps.append(f"x = {answer}")
    
    return {
        "answer": answer,
        "steps": steps
    }