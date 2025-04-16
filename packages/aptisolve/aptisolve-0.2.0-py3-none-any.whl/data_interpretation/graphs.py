def analyze_line_graph(x_values, y_values, question):
    """
    Analyze line graph data and answer questions based on it.
    
    Args:
        x_values (list): Values on the x-axis
        y_values (list): Values on the y-axis
        question (str): The question to be answered based on the graph
        
    Returns:
        dict: A dictionary containing the answer and steps to solve
    """
    steps = [
        "1. Understand the graph axes and units",
        "2. Identify trends in the data (increasing, decreasing, fluctuating)",
        "3. Find specific points of interest (peaks, troughs, intersections)",
        "4. Calculate rates of change if needed",
        "5. Formulate the answer based on the analysis"
    ]
    
    # Placeholder implementation
    answer = "Placeholder answer based on line graph analysis"
    
    return {
        "answer": answer,
        "steps": steps,
        "practice_tip": "Look for patterns and trends in line graphs rather than focusing on individual data points."
    }

def find_growth_rate(x_values, y_values, start_index, end_index):
    """
    Calculate the growth rate between two points on a graph.
    
    Args:
        x_values (list): Values on the x-axis
        y_values (list): Values on the y-axis
        start_index (int): Index of the starting point
        end_index (int): Index of the ending point
        
    Returns:
        dict: A dictionary containing the growth rate and calculation steps
    """
    steps = []
    
    try:
        start_x = x_values[start_index]
        start_y = y_values[start_index]
        end_x = x_values[end_index]
        end_y = y_values[end_index]
        
        steps.append(f"1. Identify starting point: ({start_x}, {start_y})")
        steps.append(f"2. Identify ending point: ({end_x}, {end_y})")
        
        if end_y == start_y:
            growth_rate = 0
            steps.append("3. No change in y-values, growth rate is 0")
        else:
            absolute_change = end_y - start_y
            steps.append(f"3. Calculate absolute change: {end_y} - {start_y} = {absolute_change}")
            
            percentage_change = (absolute_change / start_y) * 100
            steps.append(f"4. Calculate percentage change: ({absolute_change} / {start_y}) * 100 = {percentage_change:.2f}%")
            
            time_period = end_x - start_x
            steps.append(f"5. Calculate time period: {end_x} - {start_x} = {time_period}")
            
            if time_period == 0:
                growth_rate = "Undefined (instantaneous change)"
                steps.append("6. Time period is 0, growth rate is undefined")
            else:
                growth_rate = percentage_change / time_period
                steps.append(f"6. Calculate growth rate per unit time: {percentage_change:.2f}% / {time_period} = {growth_rate:.2f}% per unit")
        
        return {
            "growth_rate": growth_rate,
            "steps": steps,
            "practice_tip": "When calculating growth rates, always consider the starting value as the base for percentage calculations."
        }
    except IndexError:
        return {
            "growth_rate": "Error: Index out of range",
            "steps": ["Error: The provided indices are out of range for the given data."],
            "practice_tip": "Always verify that your indices are within the valid range for the dataset."
        }