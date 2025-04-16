from typing import Dict, Union, List

def calculate_average(numbers: List[float]) -> Dict[str, Union[float, List[str]]]:
    steps = []
    steps.append(f"Calculating the average of {numbers}")
    
    total = sum(numbers)
    count = len(numbers)
    
    if count == 0:
        steps.append("Error: Cannot calculate average of an empty list")
        return {
            "answer": None,
            "steps": steps
        }
    
    average = total / count
    
    steps.append(f"Step 1: Calculate the sum of all numbers")
    steps.append(f"Sum = {' + '.join(map(str, numbers))} = {total}")
    
    steps.append(f"Step 2: Divide the sum by the count of numbers")
    steps.append(f"Average = {total} ÷ {count} = {average}")
    
    return {
        "answer": average,
        "steps": steps
    }

def calculate_weighted_average(values: List[float], weights: List[float]) -> Dict[str, Union[float, List[str]]]:
    steps = []
    steps.append(f"Calculating the weighted average")
    steps.append(f"Values: {values}")
    steps.append(f"Weights: {weights}")
    
    if len(values) != len(weights):
        steps.append("Error: The number of values must match the number of weights")
        return {
            "answer": None,
            "steps": steps
        }
    
    weighted_sum = 0
    total_weight = 0
    
    steps.append(f"Step 1: Multiply each value by its corresponding weight")
    for i in range(len(values)):
        weighted_sum += values[i] * weights[i]
        total_weight += weights[i]
        steps.append(f"  {values[i]} × {weights[i]} = {values[i] * weights[i]}")
    
    steps.append(f"Step 2: Calculate the sum of weighted values")
    steps.append(f"Sum of weighted values = {weighted_sum}")
    
    steps.append(f"Step 3: Calculate the sum of weights")
    steps.append(f"Sum of weights = {total_weight}")
    
    if total_weight == 0:
        steps.append("Error: The sum of weights cannot be zero")
        return {
            "answer": None,
            "steps": steps
        }
    
    weighted_average = weighted_sum / total_weight
    
    steps.append(f"Step 4: Divide the sum of weighted values by the sum of weights")
    steps.append(f"Weighted average = {weighted_sum} ÷ {total_weight} = {weighted_average}")
    
    return {
        "answer": weighted_average,
        "steps": steps
    }