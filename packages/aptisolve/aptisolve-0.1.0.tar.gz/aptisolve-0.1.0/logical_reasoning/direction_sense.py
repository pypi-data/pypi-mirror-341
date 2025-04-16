from typing import List, Dict, Union
import random
import math

def solve_direction_problem(start_point: str, movements: List[str]) -> Dict[str, Union[str, List[str], float]]:
    """Solve direction sense problems with detailed steps"""
    # Define direction vectors (North, East, South, West)
    directions = {
        "north": (0, 1),
        "east": (1, 0),
        "south": (0, -1),
        "west": (-1, 0)
    }
    
    # Initialize position
    x, y = 0, 0
    current_direction = "north"  # Default facing north
    
    steps = [
        "Method to solve Direction Sense problems:",
        "1. Start at origin (0, 0) facing North",
        "2. Track each movement and direction change",
        "3. Calculate final position and direction",
        "",
        f"Starting point: {start_point}",
        "Initial direction: North",
        "",
        "Step-by-step movements:"
    ]
    
    # Process each movement
    for i, movement in enumerate(movements):
        steps.append(f"Movement {i+1}: {movement}")
        
        if "turn" in movement.lower() or "rotate" in movement.lower():
            # Handle direction changes
            if "right" in movement.lower():
                if current_direction == "north": current_direction = "east"
                elif current_direction == "east": current_direction = "south"
                elif current_direction == "south": current_direction = "west"
                elif current_direction == "west": current_direction = "north"
                steps.append(f"  → Turned right, now facing {current_direction.capitalize()}")
                
            elif "left" in movement.lower():
                if current_direction == "north": current_direction = "west"
                elif current_direction == "east": current_direction = "north"
                elif current_direction == "south": current_direction = "east"
                elif current_direction == "west": current_direction = "south"
                steps.append(f"  → Turned left, now facing {current_direction.capitalize()}")
                
        elif any(d in movement.lower() for d in directions.keys()):
            # Extract direction and distance
            parts = movement.lower().split()
            distance = 1  # Default distance
            
            for part in parts:
                if part.isdigit():
                    distance = int(part)
                    break
            
            for direction in directions:
                if direction in movement.lower():
                    dx, dy = directions[direction]
                    x += dx * distance
                    y += dy * distance
                    steps.append(f"  → Moved {distance} units {direction.capitalize()}")
                    steps.append(f"  → New position: ({x}, {y})")
                    break
        
        steps.append("")
    
    # Calculate final position relative to start
    distance_from_start = math.sqrt(x**2 + y**2)
    
    # Determine final direction from start
    if x == 0 and y == 0:
        final_direction = "Same as starting point"
    elif x == 0:
        final_direction = "North" if y > 0 else "South"
    elif y == 0:
        final_direction = "East" if x > 0 else "West"
    else:
        if x > 0 and y > 0: final_direction = "North-East"
        elif x > 0 and y < 0: final_direction = "South-East"
        elif x < 0 and y > 0: final_direction = "North-West"
        else: final_direction = "South-West"
    
    steps.append("Final Analysis:")
    steps.append(f"Starting point: {start_point}")
    steps.append(f"Final position: ({x}, {y})")
    steps.append(f"Distance from start: {distance_from_start:.2f} units")
    steps.append(f"Final direction from start: {final_direction}")
    steps.append(f"Facing direction: {current_direction.capitalize()}")
    
    return {
        "final_position": (x, y),
        "distance": round(distance_from_start, 2),
        "direction_from_start": final_direction,
        "facing_direction": current_direction,
        "steps": steps,
        "practice_tip": "Draw a coordinate grid with North as +y axis to visualize movements."
    }

def generate_direction_question(difficulty: str = "medium") -> Dict[str, Union[str, List[str], str]]:
    """Generate a direction sense question with varying difficulty"""
    # Define templates for different difficulty levels
    templates = {
        "easy": [
            {
                "start": "Point A",
                "movements": [
                    "Walk 2 steps North",
                    "Turn right",
                    "Walk 3 steps East"
                ],
                "question": "In which direction is Point A from the final position?",
                "answer": "South-West",
                "explanation": "Starting at A, moving 2 steps North and 3 steps East puts you at position (3, 2). From this position, Point A is in the South-West direction."
            }
        ],
        "medium": [
            {
                "start": "School",
                "movements": [
                    "Walk 4 steps North",
                    "Turn right",
                    "Walk 3 steps East",
                    "Turn right",
                    "Walk 2 steps South"
                ],
                "question": "In which direction is School from the final position?",
                "answer": "South-West",
                "explanation": "Starting at School, moving 4 steps North, 3 steps East, and 2 steps South puts you at position (3, 2). From this position, School is in the South-West direction."
            }
        ],
        "hard": [
            {
                "start": "Office",
                "movements": [
                    "Walk 3 steps East",
                    "Turn left",
                    "Walk 4 steps North",
                    "Turn left",
                    "Walk 6 steps West",
                    "Turn left",
                    "Walk 2 steps South"
                ],
                "question": "In which direction is Office from the final position?",
                "answer": "South-East",
                "explanation": "Starting at Office, after all movements, you end at position (-3, 2). From this position, Office (0,0) is in the South-East direction."
            }
        ]
    }
    
    # Select a template based on difficulty
    selected_template = random.choice(templates.get(difficulty, templates["medium"]))
    
    # Generate options (including the correct answer)
    directions = ["North", "South", "East", "West", "North-East", "North-West", "South-East", "South-West"]
    correct_answer = selected_template["answer"]
    wrong_options = random.sample([d for d in directions if d != correct_answer], 3)
    
    all_options = wrong_options + [correct_answer]
    random.shuffle(all_options)
    
    # Find index of correct answer
    correct_index = all_options.index(correct_answer)
    
    return {
        "start": selected_template["start"],
        "movements": selected_template["movements"],
        "question": selected_template["question"],
        "options": all_options,
        "correct_answer": correct_answer,
        "correct_option": chr(65 + correct_index),  # A, B, C, D
        "explanation": selected_template["explanation"],
        "difficulty": difficulty
    }