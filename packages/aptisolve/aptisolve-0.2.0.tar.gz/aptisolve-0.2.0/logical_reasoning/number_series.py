from typing import List, Dict, Union

def identify_pattern(sequence: List[int]) -> Dict[str, Union[str, int, List[str]]]:
    """
    Identify the pattern in a number series and predict the next number
    """
    steps = []
    steps.append(f"Analyzing sequence: {sequence}")
    
    # Check for arithmetic progression
    if len(sequence) >= 2:
        differences = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
        if all(diff == differences[0] for diff in differences):
            common_difference = differences[0]
            next_number = sequence[-1] + common_difference
            steps.append(f"Found constant difference: {common_difference}")
            steps.append(f"This is an arithmetic sequence")
            steps.append(f"Next number = Last number + Common difference")
            steps.append(f"Next number = {sequence[-1]} + {common_difference} = {next_number}")
            
            return {
                "pattern": "Arithmetic Progression",
                "next_number": next_number,
                "common_difference": common_difference,
                "steps": steps
            }
    
    # Check for geometric progression
    if len(sequence) >= 2 and all(x != 0 for x in sequence):
        ratios = [sequence[i+1] / sequence[i] for i in range(len(sequence)-1)]
        if all(abs(ratio - ratios[0]) < 0.0001 for ratio in ratios):
            common_ratio = ratios[0]
            next_number = int(sequence[-1] * common_ratio)
            steps.append(f"Found constant ratio: {common_ratio}")
            steps.append(f"This is a geometric sequence")
            steps.append(f"Next number = Last number × Common ratio")
            steps.append(f"Next number = {sequence[-1]} × {common_ratio} = {next_number}")
            
            return {
                "pattern": "Geometric Progression",
                "next_number": next_number,
                "common_ratio": common_ratio,
                "steps": steps
            }
    
    # Check for Fibonacci-like sequence
    if len(sequence) >= 3:
        if all(sequence[i+2] == sequence[i+1] + sequence[i] for i in range(len(sequence)-2)):
            next_number = sequence[-1] + sequence[-2]
            steps.append("Found Fibonacci-like pattern")
            steps.append(f"Next number = Sum of last two numbers")
            steps.append(f"Next number = {sequence[-1]} + {sequence[-2]} = {next_number}")
            
            return {
                "pattern": "Fibonacci Sequence",
                "next_number": next_number,
                "steps": steps
            }
    
    # If no specific pattern is found
    steps.append("No standard pattern identified")
    next_number = sequence[-1]  # Default to repeating last number
    
    return {
        "pattern": "No standard pattern identified",
        "next_number": next_number,
        "steps": steps
    }

def generate_sequence(pattern_type: str, start: int, length: int) -> Dict[str, Union[List[int], List[str]]]:
    """
    Generate a sequence based on the specified pattern type
    """
    steps = []
    sequence = []
    
    if pattern_type.lower() == "arithmetic":
        common_difference = 2
        for i in range(length):
            sequence.append(start + i * common_difference)
        steps.append(f"Generated arithmetic sequence with first term {start} and common difference {common_difference}")
    
    elif pattern_type.lower() == "geometric":
        common_ratio = 2
        for i in range(length):
            sequence.append(start * (common_ratio ** i))
        steps.append(f"Generated geometric sequence with first term {start} and common ratio {common_ratio}")
    
    elif pattern_type.lower() == "fibonacci":
        if length >= 1:
            sequence.append(start)
        if length >= 2:
            sequence.append(start + 1)
        for i in range(2, length):
            sequence.append(sequence[i-1] + sequence[i-2])
        steps.append(f"Generated Fibonacci-like sequence starting with {start}")
    
    else:
        steps.append(f"Unknown pattern type: {pattern_type}")
        return {
            "sequence": [],
            "steps": steps
        }
    
    steps.append(f"Generated sequence: {sequence}")
    
    return {
        "sequence": sequence,
        "steps": steps
    }