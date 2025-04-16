def analyze_pie_chart(categories, values, question):
    """
    Analyze pie chart data and answer questions based on it.
    
    Args:
        categories (list): List of categories in the pie chart
        values (list): List of values corresponding to each category
        question (str): The question to be answered based on the chart
        
    Returns:
        dict: A dictionary containing the answer and steps to solve
    """
    steps = [
        "1. Calculate the total sum of all values",
        "2. Calculate the percentage for each category",
        "3. Identify the relevant categories for the question",
        "4. Apply appropriate calculations if needed",
        "5. Formulate the answer"
    ]
    
    # Placeholder implementation
    total = sum(values)
    percentages = [round((value / total) * 100, 2) for value in values]
    
    # Create a mapping of categories to their percentages
    category_percentages = dict(zip(categories, percentages))
    
    answer = f"Placeholder answer based on pie chart analysis. The percentages are: {category_percentages}"
    
    return {
        "answer": answer,
        "steps": steps,
        "practice_tip": "In pie charts, focus on the relative proportions rather than absolute values."
    }

def find_largest_segment(categories, values):
    """
    Find the largest segment in a pie chart.
    
    Args:
        categories (list): List of categories in the pie chart
        values (list): List of values corresponding to each category
        
    Returns:
        dict: A dictionary containing the largest segment and calculation steps
    """
    steps = [
        f"1. Identify all categories and their values: {dict(zip(categories, values))}"
    ]
    
    if not categories or not values or len(categories) != len(values):
        return {
            "largest_segment": "Error: Invalid input data",
            "steps": ["Error: Categories and values must be non-empty lists of the same length."],
            "practice_tip": "Always ensure your data is complete and properly formatted."
        }
    
    max_value = max(values)
    max_index = values.index(max_value)
    max_category = categories[max_index]
    
    steps.append(f"2. Find the maximum value: {max_value}")
    steps.append(f"3. Identify the category with the maximum value: {max_category}")
    
    total = sum(values)
    percentage = (max_value / total) * 100
    
    steps.append(f"4. Calculate the total sum of all values: {total}")
    steps.append(f"5. Calculate the percentage of the largest segment: ({max_value} / {total}) * 100 = {percentage:.2f}%")
    
    return {
        "largest_segment": max_category,
        "value": max_value,
        "percentage": round(percentage, 2),
        "steps": steps,
        "practice_tip": "The largest segment in a pie chart represents the category with the highest proportion."
    }