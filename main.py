import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

from context import UserSessionContext
from config import config # Import the run_config from config.py

# Import refactored tools
from tools.goal_analyzer_tool import GoalAnalyzerTool
from tools.meal_planner_tool import MealPlannerTool
from tools.workout_recommender_tool import WorkoutRecommenderTool
from tools.checkin_scheduler_tool import CheckinSchedulerTool
from tools.progress_tracker_tool import ProgressTrackerTool

# Import specialized agents
from agents01.escalation_agent import EscalationAgent
from agents01.nutrition_expert_agent import NutritionExpertAgent
from agents01.injury_support_agent import InjurySupportAgent
from agents01.main_agent import HealthWellnessAgent # Import the actual agent class

# Instantiate tools
goal_analyzer_tool = GoalAnalyzerTool
meal_planner_tool = MealPlannerTool
workout_recommender_tool = WorkoutRecommenderTool
checkin_scheduler_tool = CheckinSchedulerTool
progress_tracker_tool = ProgressTrackerTool

# Instantiate specialized agents
escalation_agent = EscalationAgent()
nutrition_expert_agent = NutritionExpertAgent()
injury_support_agent = InjurySupportAgent()

def main():
    print("Welcome to the Health & Wellness Planner Agent!")
    print("Type 'quit' to exit.")

    user_context = UserSessionContext(name="Test User", uid=456)

    main_agent_instance = HealthWellnessAgent()
    
    # Assign the instantiated tools and handoff agents directly to the main_agent_instance
    main_agent_instance.tools = [
        goal_analyzer_tool,
        meal_planner_tool,
        workout_recommender_tool,
        checkin_scheduler_tool,
        progress_tracker_tool,
    ]
    main_agent_instance.handoff_to_agents = [
        escalation_agent,
        nutrition_expert_agent,
        injury_support_agent,
    ]
    
    # Initialize the main agent with the user context if needed
    # This might need to be called within the run loop or passed through the runner
    # main_agent_instance.init_session_context(user_context)

    # In a full implementation, you'd manage threads or sessions for each user
    # For this CLI example, we'll simulate a single continuous conversation

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        # Assuming run_sync handles the agent's internal logic, including tool calls and handoffs
        result = Runner.run_sync(main_agent_instance, user_input, run_config=config, context=user_context) # Pass user_context to the run
        print(f"Assistant: {result.final_output}")
        
        # Handoffs are typically handled by the framework and result in a change of the active agent
        # or a specific output. The current `openai_agents` library doesn't expose a direct
        # mechanism for external `main` loop to check for handoff explicitly on return of `run_sync`.
        # This part might need custom logic within the `on_message` or `_run` of the agent.

if __name__ == "__main__":
    main()