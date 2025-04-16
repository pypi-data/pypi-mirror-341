from typing import Dict, Union, List

def calculate_speed(distance: float, time: float) -> Dict[str, Union[float, List[str]]]:
    steps = []
    steps.append(f"Calculating speed from distance and time")
    steps.append(f"Given: Distance = {distance} units, Time = {time} units")
    
    if time <= 0:
        steps.append("Error: Time must be greater than zero")
        return {"answer": "Error: Time must be greater than zero", "steps": steps}
    
    speed = distance / time
    
    steps.append(f"Step 1: Apply the formula Speed = Distance ÷ Time")
    steps.append(f"Speed = {distance} ÷ {time} = {speed} units per time unit")
    
    return {
        "answer": speed,
        "steps": steps
    }

def calculate_distance(speed: float, time: float) -> Dict[str, Union[float, List[str]]]:
    steps = []
    steps.append(f"Calculating distance from speed and time")
    steps.append(f"Given: Speed = {speed} units per time unit, Time = {time} units")
    
    distance = speed * time
    
    steps.append(f"Step 1: Apply the formula Distance = Speed × Time")
    steps.append(f"Distance = {speed} × {time} = {distance} units")
    
    return {
        "answer": distance,
        "steps": steps
    }

def calculate_time(distance: float, speed: float) -> Dict[str, Union[float, List[str]]]:
    steps = []
    steps.append(f"Calculating time from distance and speed")
    steps.append(f"Given: Distance = {distance} units, Speed = {speed} units per time unit")
    
    if speed <= 0:
        steps.append("Error: Speed must be greater than zero")
        return {"answer": "Error: Speed must be greater than zero", "steps": steps}
    
    time = distance / speed
    
    steps.append(f"Step 1: Apply the formula Time = Distance ÷ Speed")
    steps.append(f"Time = {distance} ÷ {speed} = {time} time units")
    
    return {
        "answer": time,
        "steps": steps
    }