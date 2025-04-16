from typing import List, Dict, Union

def convert_base(number: int, to_base: int = 2, from_base: int = 10) -> Dict[str, Union[str, List[str]]]:
    """Convert a number from one base to another with detailed steps"""
    steps = []
    steps.append(f"Converting {number} from base {from_base} to base {to_base}")

    # Handle decimal to binary specifically
    if from_base == 10 and to_base == 2:
        binary = bin(number)[2:]
        steps.append(f"Step 1: Divide {number} by 2 repeatedly")
        steps.append("Division steps:")
        temp = number
        while temp > 0:
            steps.append(f"{temp} ÷ 2 = {temp//2} with remainder {temp%2}")
            temp = temp // 2
        steps.append(f"Final binary representation: {binary}")
        return {"answer": binary, "steps": steps}

    # Handle binary to decimal conversion
    if from_base == 2 and to_base == 10:
        steps.append("Step 1: Convert each binary digit to its decimal value")
        decimal = 0
        binary_str = str(number)
        steps.append("Position weights (from right to left):")
        
        for i, digit in enumerate(reversed(binary_str)):
            weight = 2**i
            steps.append(f"{digit} × 2^{i} = {int(digit)*weight}")
            decimal += int(digit) * weight
            
        steps.append(f"Sum all values: {decimal}")
        return {"answer": str(decimal), "steps": steps}

    # General base conversion
    if from_base == 10:
        result = ""
        quotient = number
        
        steps = [
            "Method to convert from Base 10 to another base:",
            f"Formula: Repeatedly divide by {to_base} and collect remainders in reverse order",
            "",
            f"Given number: {number} (Base 10)",
            f"Target base: {to_base}",
            "",
            "Step-by-step division:"
        ]
        
        division_steps = []
        while quotient > 0:
            remainder = quotient % to_base
            if remainder > 9:
                remainder_char = chr(ord('A') + remainder - 10)
            else:
                remainder_char = str(remainder)
            division_steps.append(f"{quotient} ÷ {to_base} = {quotient // to_base} with remainder {remainder} ({remainder_char})")
            result = remainder_char + result
            quotient //= to_base
        
        steps.extend(division_steps)
        steps.append("")
        steps.append(f"Reading remainders from bottom to top: {result}")
        steps.append("")
        steps.append(f"Final Answer: {result} (Base {to_base})")
        
        return {
            "answer": result,
            "steps": steps,
            "formula": f"Repeatedly divide by {to_base} and collect remainders in reverse order",
            "practice_tip": "When converting manually, write each division step clearly and collect remainders from bottom to top."
        }
    else:
        # Convert from any base to decimal first
        decimal = 0
        digits = str(number)[::-1]
        
        steps = [
            f"Method to convert from Base {from_base} to Base {to_base}:",
            f"Step 1: First convert from Base {from_base} to Decimal (Base 10)",
            f"Formula: Multiply each digit by its place value and sum",
            "",
            f"Given number: {number} (Base {from_base})",
            "",
            "Converting to decimal:"
        ]
        
        for i, digit in enumerate(digits):
            if digit.isalpha():
                digit_value = ord(digit.upper()) - ord('A') + 10
            else:
                digit_value = int(digit)
            place_value = from_base ** i
            decimal += digit_value * place_value
            steps.append(f"{digit_value} × {from_base}^{i} = {digit_value * place_value}")
        
        # Then convert decimal to target base
        return convert_base(decimal, to_base, 10)

def find_lcm_hcf(a: int, b: int) -> Dict[str, Union[int, List[str]]]:
    """Calculate LCM and HCF with detailed steps"""
    original_a, original_b = a, b
    
    steps = [
        "Method to find HCF and LCM:",
        "For HCF: Use Euclidean Algorithm (repeated division)",
        "For LCM: Use formula LCM(a,b) = (a × b) ÷ HCF(a,b)",
        "",
        f"Given numbers: {a} and {b}",
        "",
        "Step 1: Find HCF using Euclidean Algorithm"
    ]
    
    euclidean_steps = []
    while b:
        euclidean_steps.append(f"{a} = {b} × {a // b} + {a % b}")
        a, b = b, a % b
    
    hcf = a
    steps.extend(euclidean_steps)
    steps.append(f"HCF = {hcf}")
    steps.append("")
    
    lcm = (original_a * original_b) // hcf
    
    steps.append("Step 2: Find LCM using the formula")
    steps.append(f"LCM = (a × b) ÷ HCF")
    steps.append(f"LCM = ({original_a} × {original_b}) ÷ {hcf}")
    steps.append(f"LCM = {original_a * original_b} ÷ {hcf}")
    steps.append(f"LCM = {lcm}")
    
    return {
        "hcf": hcf,
        "lcm": lcm,
        "steps": steps,
        "formula": "HCF: Euclidean Algorithm\nLCM: (a × b) ÷ HCF"
    }

def check_divisibility(number: int, divisor: int) -> Dict[str, Union[bool, List[str]]]:
    """Check if a number is divisible by another with explanation of the rule"""
    result = number % divisor == 0
    
    rules = {
        2: "A number is divisible by 2 if its last digit is even (0, 2, 4, 6, or 8).",
        3: "A number is divisible by 3 if the sum of its digits is divisible by 3.",
        4: "A number is divisible by 4 if the last two digits form a number divisible by 4.",
        5: "A number is divisible by 5 if its last digit is 0 or 5.",
        6: "A number is divisible by 6 if it is divisible by both 2 and 3.",
        7: "A number is divisible by 7 if the alternating sum of groups of 3 digits is divisible by 7.",
        8: "A number is divisible by 8 if the last three digits form a number divisible by 8.",
        9: "A number is divisible by 9 if the sum of its digits is divisible by 9.",
        10: "A number is divisible by 10 if its last digit is 0.",
        11: "A number is divisible by 11 if the alternating sum of its digits is divisible by 11."
    }
    
    steps = [f"Checking if {number} is divisible by {divisor}:", ""]
    
    if divisor in rules:
        steps.append(f"Divisibility rule for {divisor}: {rules[divisor]}")
        steps.append("")
        
        if divisor == 2:
            last_digit = number % 10
            steps.append(f"Last digit of {number} is {last_digit}")
            steps.append(f"Is {last_digit} even? {'Yes' if last_digit in [0, 2, 4, 6, 8] else 'No'}")
        elif divisor == 3:
            digit_sum = sum(int(digit) for digit in str(number))
            steps.append(f"Sum of digits: {' + '.join(str(number))} = {digit_sum}")
            steps.append(f"Is {digit_sum} divisible by 3? {'Yes' if digit_sum % 3 == 0 else 'No'}")
        elif divisor == 4:
            last_two = number % 100
            steps.append(f"Last two digits of {number} are {last_two}")
            steps.append(f"Is {last_two} divisible by 4? {'Yes' if last_two % 4 == 0 else 'No'}")
        elif divisor == 5:
            last_digit = number % 10
            steps.append(f"Last digit of {number} is {last_digit}")
            steps.append(f"Is {last_digit} 0 or 5? {'Yes' if last_digit in [0, 5] else 'No'}")
        elif divisor == 6:
            div_by_2 = number % 2 == 0
            digit_sum = sum(int(digit) for digit in str(number))
            div_by_3 = digit_sum % 3 == 0
            steps.append(f"Is {number} divisible by 2? {'Yes' if div_by_2 else 'No'}")
            steps.append(f"Sum of digits: {' + '.join(str(number))} = {digit_sum}")
            steps.append(f"Is {digit_sum} divisible by 3? {'Yes' if div_by_3 else 'No'}")
            steps.append(f"Is {number} divisible by both 2 and 3? {'Yes' if div_by_2 and div_by_3 else 'No'}")
    
    steps.append(f"Direct check: {number} ÷ {divisor} = {number // divisor} with remainder {number % divisor}")
    steps.append(f"Is {number} divisible by {divisor}? {'Yes' if result else 'No'}")
    steps.append("")
    steps.append(f"Final Answer: {number} {'is' if result else 'is not'} divisible by {divisor}")
    
    return {
        "answer": result,
        "steps": steps,
        "rule": rules.get(divisor, "Use direct division to check.")
    }


def analyze_number(number: int, operation: str, num2: int = None) -> Dict[str, Union[str, List[str]]]:
    """Analyze number based on operation type"""
    if operation == 'base_conversion':
        return convert_base(number)
    elif operation == 'lcm' and num2:
        result = find_lcm_hcf(number, num2)
        return {"answer": result["lcm"], "steps": result["steps"]}
    elif operation == 'hcf' and num2:
        result = find_lcm_hcf(number, num2)
        return {"answer": result["hcf"], "steps": result["steps"]}
    elif operation == 'factors':
        return find_factors(number)
    elif operation == 'prime':
        return check_prime(number)
    else:
        return {"error": "Invalid operation", "steps": ["Operation not supported"]}

def find_factors(number: int) -> Dict[str, Union[List[int], List[str]]]:
    """Find factors of a number with steps"""
    factors = []
    steps = [f"Finding factors of {number}:", ""]
    
    for i in range(1, int(number ** 0.5) + 1):
        if number % i == 0:
            factors.append(i)
            steps.append(f"{number} ÷ {i} = {number//i} (Factor pair: {i}, {number//i})")
            if i != number // i:
                factors.append(number // i)
    
    factors.sort()
    steps.append("")
    steps.append(f"All factors: {factors}")
    
    return {
        "answer": factors,
        "steps": steps
    }

def check_prime(number: int) -> Dict[str, Union[bool, List[str]]]:
    """Check if a number is prime with detailed steps"""
    if number < 2:
        return {
            "answer": False,
            "steps": [f"{number} is not a prime number as it's less than 2"]
        }
    
    steps = [f"Checking if {number} is prime:", ""]
    steps.append("A prime number is only divisible by 1 and itself")
    steps.append(f"Checking divisibility up to {int(number**0.5)}")
    
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            steps.append(f"{number} is divisible by {i} ({number} ÷ {i} = {number//i})")
            steps.append(f"Therefore, {number} is not prime")
            return {
                "answer": False,
                "steps": steps
            }
    
    steps.append(f"No factors found between 2 and {int(number**0.5)}")
    steps.append(f"Therefore, {number} is prime")
    return {
        "answer": True,
        "steps": steps
    }