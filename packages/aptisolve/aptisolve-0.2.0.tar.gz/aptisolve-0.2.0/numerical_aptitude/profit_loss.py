from typing import Dict, List, Union, Any

def calculate_profit_loss(cost_price: float, selling_price: float) -> Dict[str, Any]:
    """
    Calculate profit or loss and percentage based on cost price and selling price.
    
    Args:
        cost_price (float): The cost price of the item
        selling_price (float): The selling price of the item
        
    Returns:
        dict: A dictionary containing the result, percentage, and step-by-step solution
    """
    steps = []
    
    # Input validation
    if cost_price <= 0 or selling_price < 0:
        return {
            "result": "Error: Cost price must be positive and selling price must be non-negative",
            "percentage": None,
            "steps": ["Error: Invalid input values"]
        }
    
    # Calculate the difference
    difference = selling_price - cost_price
    
    # Determine if it's a profit or loss
    if difference > 0:
        result_type = "Profit"
    elif difference < 0:
        result_type = "Loss"
        difference = abs(difference)  # Make the difference positive for calculations
    else:
        result_type = "No Profit No Loss"
    
    # Calculate the percentage
    if result_type != "No Profit No Loss":
        percentage = (difference / cost_price) * 100
    else:
        percentage = 0
    
    # Generate step-by-step solution
    steps.append(f"Step 1: Identify the Cost Price (CP) = ₹{cost_price:.2f}")
    steps.append(f"Step 2: Identify the Selling Price (SP) = ₹{selling_price:.2f}")
    steps.append(f"Step 3: Calculate the difference between SP and CP:")
    steps.append(f"         SP - CP = ₹{selling_price:.2f} - ₹{cost_price:.2f} = ₹{selling_price - cost_price:.2f}")
    
    if result_type == "Profit":
        steps.append(f"Step 4: Since SP > CP, it's a Profit of ₹{difference:.2f}")
        steps.append(f"Step 5: Calculate Profit Percentage:")
        steps.append(f"         Profit Percentage = (Profit / CP) × 100")
        steps.append(f"         Profit Percentage = (₹{difference:.2f} / ₹{cost_price:.2f}) × 100 = {percentage:.2f}%")
    elif result_type == "Loss":
        steps.append(f"Step 4: Since SP < CP, it's a Loss of ₹{difference:.2f}")
        steps.append(f"Step 5: Calculate Loss Percentage:")
        steps.append(f"         Loss Percentage = (Loss / CP) × 100")
        steps.append(f"         Loss Percentage = (₹{difference:.2f} / ₹{cost_price:.2f}) × 100 = {percentage:.2f}%")
    else:
        steps.append(f"Step 4: Since SP = CP, there is No Profit No Loss")
        steps.append(f"Step 5: Profit/Loss Percentage = 0%")
    
    return {
        "result": f"{result_type}: ₹{difference:.2f}" if result_type != "No Profit No Loss" else result_type,
        "percentage": round(percentage, 2),
        "steps": steps,
        "practice_tip": "Remember: Profit or Loss is always calculated with respect to the Cost Price."
    }

def calculate_cost_price(selling_price: float, profit_loss_percentage: float, is_profit: bool = True) -> Dict[str, Any]:
    """
    Calculate the cost price given the selling price and profit/loss percentage.
    
    Args:
        selling_price (float): The selling price of the item
        profit_loss_percentage (float): The profit or loss percentage
        is_profit (bool): True if it's a profit percentage, False if it's a loss percentage
        
    Returns:
        dict: A dictionary containing the cost price and step-by-step solution
    """
    steps = []
    
    # Input validation
    if selling_price <= 0 or profit_loss_percentage < 0:
        return {
            "cost_price": "Error: Selling price must be positive and profit/loss percentage must be non-negative",
            "steps": ["Error: Invalid input values"]
        }
    
    # Generate step-by-step solution
    steps.append(f"Step 1: Identify the Selling Price (SP) = ₹{selling_price:.2f}")
    steps.append(f"Step 2: Identify the {'Profit' if is_profit else 'Loss'} Percentage = {profit_loss_percentage:.2f}%")
    
    if is_profit:
        steps.append(f"Step 3: Use the formula: SP = CP + Profit")
        steps.append(f"Step 4: Since Profit = CP × (Profit Percentage / 100)")
        steps.append(f"Step 5: SP = CP + CP × (Profit Percentage / 100)")
        steps.append(f"Step 6: SP = CP × [1 + (Profit Percentage / 100)]")
        steps.append(f"Step 7: CP = SP / [1 + (Profit Percentage / 100)]")
        steps.append(f"Step 8: CP = ₹{selling_price:.2f} / [1 + ({profit_loss_percentage:.2f} / 100)]")
        steps.append(f"Step 9: CP = ₹{selling_price:.2f} / [1 + {profit_loss_percentage/100:.4f}]")
        steps.append(f"Step 10: CP = ₹{selling_price:.2f} / {1 + profit_loss_percentage/100:.4f}")
        
        cost_price = selling_price / (1 + profit_loss_percentage/100)
        steps.append(f"Step 11: CP = ₹{cost_price:.2f}")
    else:
        steps.append(f"Step 3: Use the formula: SP = CP - Loss")
        steps.append(f"Step 4: Since Loss = CP × (Loss Percentage / 100)")
        steps.append(f"Step 5: SP = CP - CP × (Loss Percentage / 100)")
        steps.append(f"Step 6: SP = CP × [1 - (Loss Percentage / 100)]")
        steps.append(f"Step 7: CP = SP / [1 - (Loss Percentage / 100)]")
        steps.append(f"Step 8: CP = ₹{selling_price:.2f} / [1 - ({profit_loss_percentage:.2f} / 100)]")
        steps.append(f"Step 9: CP = ₹{selling_price:.2f} / [1 - {profit_loss_percentage/100:.4f}]")
        steps.append(f"Step 10: CP = ₹{selling_price:.2f} / {1 - profit_loss_percentage/100:.4f}")
        
        cost_price = selling_price / (1 - profit_loss_percentage/100)
        steps.append(f"Step 11: CP = ₹{cost_price:.2f}")
    
    return {
        "cost_price": round(cost_price, 2),
        "steps": steps,
        "practice_tip": "Always remember to convert percentage to decimal by dividing by 100 before using in formulas."
    }

def calculate_selling_price(cost_price: float, profit_loss_percentage: float, is_profit: bool = True) -> Dict[str, Any]:
    """
    Calculate the selling price given the cost price and profit/loss percentage.
    
    Args:
        cost_price (float): The cost price of the item
        profit_loss_percentage (float): The profit or loss percentage
        is_profit (bool): True if it's a profit percentage, False if it's a loss percentage
        
    Returns:
        dict: A dictionary containing the selling price and step-by-step solution
    """
    steps = []
    
    # Input validation
    if cost_price <= 0 or profit_loss_percentage < 0:
        return {
            "selling_price": "Error: Cost price must be positive and profit/loss percentage must be non-negative",
            "steps": ["Error: Invalid input values"]
        }
    
    # Generate step-by-step solution
    steps.append(f"Step 1: Identify the Cost Price (CP) = ₹{cost_price:.2f}")
    steps.append(f"Step 2: Identify the {'Profit' if is_profit else 'Loss'} Percentage = {profit_loss_percentage:.2f}%")
    
    if is_profit:
        steps.append(f"Step 3: Calculate the Profit amount:")
        steps.append(f"         Profit = CP × (Profit Percentage / 100)")
        steps.append(f"         Profit = ₹{cost_price:.2f} × ({profit_loss_percentage:.2f} / 100)")
        steps.append(f"         Profit = ₹{cost_price:.2f} × {profit_loss_percentage/100:.4f}")
        
        profit = cost_price * (profit_loss_percentage / 100)
        steps.append(f"         Profit = ₹{profit:.2f}")
        
        steps.append(f"Step 4: Calculate the Selling Price:")
        steps.append(f"         SP = CP + Profit")
        steps.append(f"         SP = ₹{cost_price:.2f} + ₹{profit:.2f}")
        
        selling_price = cost_price + profit
        steps.append(f"         SP = ₹{selling_price:.2f}")
    else:
        steps.append(f"Step 3: Calculate the Loss amount:")
        steps.append(f"         Loss = CP × (Loss Percentage / 100)")
        steps.append(f"         Loss = ₹{cost_price:.2f} × ({profit_loss_percentage:.2f} / 100)")
        steps.append(f"         Loss = ₹{cost_price:.2f} × {profit_loss_percentage/100:.4f}")
        
        loss = cost_price * (profit_loss_percentage / 100)
        steps.append(f"         Loss = ₹{loss:.2f}")
        
        steps.append(f"Step 4: Calculate the Selling Price:")
        steps.append(f"         SP = CP - Loss")
        steps.append(f"         SP = ₹{cost_price:.2f} - ₹{loss:.2f}")
        
        selling_price = cost_price - loss
        steps.append(f"         SP = ₹{selling_price:.2f}")
    
    return {
        "selling_price": round(selling_price, 2),
        "steps": steps,
        "practice_tip": "To double-check your answer, you can verify that the profit/loss percentage calculated from CP and SP matches your input percentage."
    }

def calculate_marked_price(cost_price: float, profit_percentage: float, discount_percentage: float) -> Dict[str, Any]:
    """
    Calculate the marked price given the cost price, desired profit percentage, and discount percentage.
    
    Args:
        cost_price (float): The cost price of the item
        profit_percentage (float): The desired profit percentage after discount
        discount_percentage (float): The discount percentage offered on marked price
        
    Returns:
        dict: A dictionary containing the marked price, selling price, and step-by-step solution
    """
    steps = []
    
    # Input validation
    if cost_price <= 0 or profit_percentage < 0 or discount_percentage < 0 or discount_percentage >= 100:
        return {
            "marked_price": "Error: Invalid input values",
            "selling_price": None,
            "steps": ["Error: Cost price must be positive, percentages must be non-negative, and discount must be less than 100%"]
        }
    
    # Generate step-by-step solution
    steps.append(f"Step 1: Identify the Cost Price (CP) = ₹{cost_price:.2f}")
    steps.append(f"Step 2: Identify the desired Profit Percentage = {profit_percentage:.2f}%")
    steps.append(f"Step 3: Identify the Discount Percentage = {discount_percentage:.2f}%")
    
    steps.append(f"Step 4: Calculate the required Selling Price (SP) after discount:")
    steps.append(f"         SP = CP + Profit")
    steps.append(f"         Profit = CP × (Profit Percentage / 100)")
    steps.append(f"         Profit = ₹{cost_price:.2f} × ({profit_percentage:.2f} / 100) = ₹{cost_price * profit_percentage / 100:.2f}")
    
    selling_price = cost_price * (1 + profit_percentage / 100)
    steps.append(f"         SP = ₹{cost_price:.2f} + ₹{cost_price * profit_percentage / 100:.2f} = ₹{selling_price:.2f}")
    
    steps.append(f"Step 5: Calculate the Marked Price (MP) considering the discount:")
    steps.append(f"         SP = MP × (1 - Discount Percentage / 100)")
    steps.append(f"         MP = SP / (1 - Discount Percentage / 100)")
    steps.append(f"         MP = ₹{selling_price:.2f} / (1 - {discount_percentage:.2f} / 100)")
    steps.append(f"         MP = ₹{selling_price:.2f} / (1 - {discount_percentage/100:.4f})")
    steps.append(f"         MP = ₹{selling_price:.2f} / {1 - discount_percentage/100:.4f}")
    
    marked_price = selling_price / (1 - discount_percentage / 100)
    steps.append(f"         MP = ₹{marked_price:.2f}")
    
    steps.append(f"Step 6: Verify the calculation:")
    steps.append(f"         Discount Amount = MP × (Discount Percentage / 100)")
    steps.append(f"         Discount Amount = ₹{marked_price:.2f} × ({discount_percentage:.2f} / 100) = ₹{marked_price * discount_percentage / 100:.2f}")
    steps.append(f"         SP = MP - Discount Amount")
    steps.append(f"         SP = ₹{marked_price:.2f} - ₹{marked_price * discount_percentage / 100:.2f} = ₹{marked_price * (1 - discount_percentage / 100):.2f}")
    steps.append(f"         This matches our required SP of ₹{selling_price:.2f}")
    
    return {
        "marked_price": round(marked_price, 2),
        "selling_price": round(selling_price, 2),
        "steps": steps,
        "practice_tip": "When calculating marked price with discount, remember that the final selling price must give you the desired profit."
    }

def calculate_successive_discounts(marked_price: float, discount_percentages: List[float]) -> Dict[str, Any]:
    """
    Calculate the final price after applying successive discounts.
    
    Args:
        marked_price (float): The marked price of the item
        discount_percentages (list): List of successive discount percentages
        
    Returns:
        dict: A dictionary containing the final price and step-by-step solution
    """
    steps = []
    
    # Input validation
    if marked_price <= 0 or any(d < 0 or d >= 100 for d in discount_percentages):
        return {
            "final_price": "Error: Invalid input values",
            "steps": ["Error: Marked price must be positive and discount percentages must be between 0 and 100"]
        }
    
    # Generate step-by-step solution
    steps.append(f"Step 1: Identify the Marked Price (MP) = ₹{marked_price:.2f}")
    steps.append(f"Step 2: Identify the successive discount percentages: {', '.join([f'{d:.2f}%' for d in discount_percentages])}")
    
    current_price = marked_price
    for i, discount in enumerate(discount_percentages, 1):
        steps.append(f"Step {i+2}: Apply Discount {i} of {discount:.2f}%:")
        steps.append(f"         Discount Amount = Current Price × (Discount Percentage / 100)")
        steps.append(f"         Discount Amount = ₹{current_price:.2f} × ({discount:.2f} / 100) = ₹{current_price * discount / 100:.2f}")
        
        new_price = current_price * (1 - discount / 100)
        steps.append(f"         New Price = Current Price - Discount Amount")
        steps.append(f"         New Price = ₹{current_price:.2f} - ₹{current_price * discount / 100:.2f} = ₹{new_price:.2f}")
        
        current_price = new_price
    
    # Calculate equivalent single discount
    total_discount_percentage = (1 - current_price / marked_price) * 100
    steps.append(f"Step {len(discount_percentages)+3}: Calculate the equivalent single discount:")
    steps.append(f"         Original Price = ₹{marked_price:.2f}")
    steps.append(f"         Final Price = ₹{current_price:.2f}")
    steps.append(f"         Total Discount Amount = ₹{marked_price:.2f} - ₹{current_price:.2f} = ₹{marked_price - current_price:.2f}")
    steps.append(f"         Equivalent Single Discount Percentage = (Total Discount Amount / Original Price) × 100")
    steps.append(f"         Equivalent Single Discount Percentage = (₹{marked_price - current_price:.2f} / ₹{marked_price:.2f}) × 100 = {total_discount_percentage:.2f}%")
    
    # Alternative calculation for equivalent single discount
    steps.append(f"Step {len(discount_percentages)+4}: Alternative formula for equivalent single discount:")
    
    formula_parts = []
    for discount in discount_percentages:
        if formula_parts:
            formula_parts.append(f" + {discount:.2f}%")
        else:
            formula_parts.append(f"{discount:.2f}%")
    
    for i in range(len(discount_percentages)):
        for j in range(i+1, len(discount_percentages)):
            formula_parts.append(f" - ({discount_percentages[i]:.2f}% × {discount_percentages[j]:.2f}% / 100)")
    
    steps.append(f"         Equivalent Single Discount = {' '.join(formula_parts)}")
    
    # For two discounts, show the simplified formula
    if len(discount_percentages) == 2:
        d1, d2 = discount_percentages
        calculated_discount = d1 + d2 - (d1 * d2 / 100)
        steps.append(f"         For two discounts: Equivalent Discount = d₁ + d₂ - (d₁ × d₂ / 100)")
        steps.append(f"         Equivalent Discount = {d1:.2f}% + {d2:.2f}% - ({d1:.2f}% × {d2:.2f}% / 100)")
        steps.append(f"         Equivalent Discount = {d1:.2f}% + {d2:.2f}% - {d1 * d2 / 100:.2f}%")
        steps.append(f"         Equivalent Discount = {calculated_discount:.2f}%")
        steps.append(f"         This matches our calculated equivalent discount of {total_discount_percentage:.2f}%")
    
    return {
        "final_price": round(current_price, 2),
        "equivalent_discount_percentage": round(total_discount_percentage, 2),
        "steps": steps,
        "practice_tip": "Successive discounts are not additive. A 20% discount followed by a 10% discount is not the same as a 30% discount."
    }