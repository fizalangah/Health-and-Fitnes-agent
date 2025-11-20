from agents import Agent 
from tools.goal_analyzer_tool import GoalAnalyzerTool
from tools.meal_planner_tool import MealPlannerTool
from tools.workout_recommender_tool import WorkoutRecommenderTool
from tools.checkin_scheduler_tool import CheckinSchedulerTool
from tools.progress_tracker_tool import ProgressTrackerTool

class HealthWellnessAgent(Agent):
    name: str = "HealthWellnessAgent"

    description: str = (
        "A comprehensive AI-powered Health & Wellness Planner Agent that understands "
        "user goals, guides through multi-step planning, and provides personalized recommendations."
    )

    base_instructions: str = (
        "Your responsibilities:\n"
        "1. Collect fitness and dietary goals through multi-turn conversation.\n"
        "2. Analyze goals using the GoalAnalyzerTool.\n"
        "3. Generate customized meal and workout plans.\n"
        "4. Track progress and schedule reminders.\n"
        "5. Maintain context across interactions.\n"
        "6. Validate inputs and produce structured outputs.\n"
        "7. Hand off to specialized agents when needed (nutrition, injury, escalation).\n"
        "Always give supportive, personalized advice. Do not impersonate a medical professional."
    )

    tools = [
        GoalAnalyzerTool,
        MealPlannerTool,
        WorkoutRecommenderTool,
        CheckinSchedulerTool,
        ProgressTrackerTool,
    ]

    handoff_to_agents = []  # will be set in main.py

    def __init__(self):
        super().__init__(
            name=self.name,
            instructions=f"{self.description}\n\n{self.base_instructions}",
            tools=self.tools,
        )
