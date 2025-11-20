from pydantic import BaseModel, Field
from typing import Optional, List
from agents import function_tool

class FitnessGoalInput(BaseModel):
    original_description: str = Field(..., description="The original description of the fitness goal.")
    # Add other expected fields for a structured fitness goal here
    # Example:
    # target_weight_loss_kg: Optional[float] = None
    # goal_type: Optional[str] = None

    class Config:
        extra = "forbid" # Disallow additional properties

@function_tool(
    name_override="WorkoutRecommenderTool",
    description_override="Recommends a workout plan based on the user's parsed goals. This tool takes structured fitness goals and suggests a suitable workout regimen.",
)
async def WorkoutRecommenderTool(fitness_goal: FitnessGoalInput, current_fitness_level: Optional[str] = None, available_equipment: Optional[List[str]] = None, time_per_session_minutes: Optional[int] = None) -> dict:
    """
    Recommends a workout plan based on the user's parsed goals.
    This tool takes structured fitness goals and suggests a suitable workout regimen.
    """
    # In a real implementation, this would use a more sophisticated recommendation engine
    # based on exercise science principles, user data, and available resources.
    # For now, we provide a placeholder.

    plan_details = {
        "goal": fitness_goal.original_description, # Access field from Pydantic model
        "level": current_fitness_level if current_fitness_level else "all levels",
        "frequency": "3-4 times per week",
        "duration_per_session": f"{time_per_session_minutes} minutes" if time_per_session_minutes else "60 minutes",
        "equipment": ", ".join(available_equipment) if available_equipment else "bodyweight, basic gym equipment",
        "exercises": [
            "Warm-up: 5-10 minutes light cardio and dynamic stretches",
            "Strength Training: (e.g., Squats, Push-ups, Rows, Lunges - 3 sets of 8-12 reps)",
            "Cardio: 20-30 minutes of moderate intensity (e.g., jogging, cycling)",
            "Cool-down: 5-10 minutes static stretches"
        ],
        "notes": "Adjust intensity and volume based on how you feel. Consult a professional before starting any new workout regimen."
    }

    workout_plan = {
        "recommended_plan": plan_details,
        "plan_id": "WKPLN_001",
        "creation_date": "2025-11-20"
    }

    return workout_plan