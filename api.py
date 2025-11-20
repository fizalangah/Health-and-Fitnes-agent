from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime # Added datetime import

from agents01.main_agent import HealthWellnessAgent
from context import UserSessionContext

app = FastAPI()

# In-memory store for user sessions (for demonstration purposes)
# Production kay liye, isko database ya kisi aur persistent storage say replace karna hoga
user_sessions: Dict[str, UserSessionContext] = {}

# Agent ko initialize karain. Ye production main theek tareeqay say manage karna hoga.
health_wellness_agent_instance = HealthWellnessAgent()

class GoalRequest(BaseModel):
    user_id: str
    user_name: str
    goal_description: str
    diet_preferences: Optional[str] = None

class PlanResponse(BaseModel):
    user_id: str
    status: str
    message: str
    meal_plan: Optional[List[str]] = None
    workout_plan: Optional[Dict[str, Any]] = None
    # Aur bhi fields jo aap return karna chahtay hain

# Pydantic models for Check-in Scheduler Tool
class CheckinRequest(BaseModel):
    user_id: str
    checkin_date: str # YYYY-MM-DD format
    notes: Optional[str] = None

class CheckinResponse(BaseModel):
    user_id: str
    status: str
    message: str
    scheduled_checkins: List[Dict[str, str]]

# Pydantic models for Progress Tracker Tool
class ProgressLog(BaseModel):
    timestamp: str
    entry: str

class ProgressUpdateRequest(BaseModel):
    user_id: str
    log_entry: str

class ProgressResponse(BaseModel):
    user_id: str
    status: str
    message: str
    progress_logs: List[ProgressLog]

# Pydantic models for Handoffs
class HandoffRequest(BaseModel):
    user_id: str
    reason: str
    details: Optional[str] = None

class HandoffResponse(BaseModel):
    user_id: str
    status: str
    message: str
    handoff_type: str
    expert_contact: Optional[str] = None

@app.post("/set_goal", response_model=PlanResponse) # Add response_model for better docs
async def set_user_goal(request: GoalRequest):
    try:
        user_id = request.user_id
        
        # Get or create user session context
        if user_id not in user_sessions:
            user_sessions[user_id] = UserSessionContext(
                name=request.user_name,
                uid=hash(user_id) % (10**8),
            )
        user_context = user_sessions[user_id]

        # Update context with current request data
        # Note: This simply updates the context's goal and diet preferences.
        # A real GoalAnalyzerTool would parse and validate the goal_description.
        user_context.goal = {"description": request.goal_description}
        user_context.diet_preferences = request.diet_preferences

        # --- Simulating Agent's Internal Tool Orchestration ---
        # A proper HealthWellnessAgent would have an internal method (e.g., `ainvoke` or `process_goal`)
        # that orchestrates its tools (GoalAnalyzerTool, MealPlannerTool, WorkoutRecommenderTool).
        # Since that method is not exposed in the provided HealthWellnessAgent class,
        # we are simulating the outcome of those tools by directly modifying the UserSessionContext.

        # 1. Goal Analysis (Simulated by updating context directly)
        # In a real scenario, GoalAnalyzerTool would process request.goal_description
        # and update user_context.goal with a structured, analyzed goal.
        user_context.goal["status"] = "analyzed" # Mark as analyzed

        # 2. Meal Plan Generation (Simulated)
        # MealPlannerTool would use user_context.diet_preferences and user_context.goal
        # to generate a detailed meal plan.
        user_context.meal_plan = [
            f"Monday: Healthy meal based on goal: {request.goal_description} & preference: {request.diet_preferences}",
            f"Tuesday: Nutritious meal for {request.diet_preferences}",
            f"Wednesday: Balanced meal for {request.diet_preferences}",
            "Thursday: Protein-rich dinner recommendation",
            "Friday: Light and fresh meal idea",
            "Saturday: Moderately flexible meal",
            "Sunday: Family-friendly healthy option"
        ]
        
        # 3. Workout Plan Recommendation (Simulated)
        # WorkoutRecommenderTool would use user_context.goal to create a workout plan.
        user_context.workout_plan = {
            "Monday": f"Strength Training (Full Body) for goal: {request.goal_description}",
            "Tuesday": "Cardio (Running 45 min)",
            "Wednesday": "Rest / Active Recovery (e.g., light stretching)",
            "Thursday": "Yoga / Flexibility session",
            "Friday": "High-Intensity Interval Training (HIIT)",
            "Saturday": "Long Walk / Hike (Outdoor activity)",
            "Sunday": "Complete Rest"
        }
        
        # --- End of Simulation ---

        # Update the session with the modified context (redundant if context is mutable, but good practice for clarity)
        user_sessions[user_id] = user_context

        return PlanResponse(
            user_id=user_id,
            status="success",
            message="Goals processed and plans generated by agent (simulated).",
            meal_plan=user_context.meal_plan,
            workout_plan=user_context.workout_plan
        )
    except Exception as e:
        # Robust Error Handling
        print(f"Error processing /set_goal for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/schedule_checkin", response_model=CheckinResponse)
async def schedule_checkin(request: CheckinRequest):
    try:
        user_id = request.user_id
        if user_id not in user_sessions:
            raise HTTPException(status_code=404, detail="User session not found. Please set a goal first.")
        user_context = user_sessions[user_id]

        # Simulate CheckinSchedulerTool
        # In a real tool, this would schedule a reminder or store the check-in details.
        # Assuming UserSessionContext can store scheduled_checkins
        if not hasattr(user_context, 'scheduled_checkins') or user_context.scheduled_checkins is None:
            user_context.scheduled_checkins = []
        user_context.scheduled_checkins.append({"date": request.checkin_date, "notes": request.notes})

        user_sessions[user_id] = user_context # Update session

        return CheckinResponse(
            user_id=user_id,
            status="success",
            message=f"Check-in scheduled for {request.checkin_date}.",
            scheduled_checkins=user_context.scheduled_checkins
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error scheduling check-in for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/track_progress", response_model=ProgressResponse)
async def track_progress(request: ProgressUpdateRequest):
    try:
        user_id = request.user_id
        if user_id not in user_sessions:
            raise HTTPException(status_code=404, detail="User session not found. Please set a goal first.")
        user_context = user_sessions[user_id]

        # Simulate ProgressTrackerTool
        # This tool would typically add a log entry to the user's progress.
        # Assuming UserSessionContext can store progress_logs (List[Dict[str, str]])
        if not hasattr(user_context, 'progress_logs') or user_context.progress_logs is None:
            user_context.progress_logs = []
        user_context.progress_logs.append({"timestamp": datetime.now().isoformat(), "entry": request.log_entry})

        user_sessions[user_id] = user_context # Update session

        return ProgressResponse(
            user_id=user_id,
            status="success",
            message="Progress logged successfully.",
            progress_logs=user_context.progress_logs # Direct return of list of dicts
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error tracking progress for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/get_progress/{user_id}", response_model=ProgressResponse)
async def get_progress(user_id: str):
    try:
        if user_id not in user_sessions:
            raise HTTPException(status_code=404, detail="User session not found. Please set a goal first.")
        user_context = user_sessions[user_id]

        # Return existing progress logs
        return ProgressResponse(
            user_id=user_id,
            status="success",
            message="Progress logs retrieved successfully.",
            progress_logs=user_context.progress_logs if user_context.progress_logs else []
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error retrieving progress for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/request_human_coach", response_model=HandoffResponse)
async def request_human_coach(request: HandoffRequest):
    try:
        user_id = request.user_id
        if user_id not in user_sessions:
            # It's possible a user requests a coach without a full session, depending on design.
            # For this example, we'll allow it but note session state.
            pass # Or create a minimal session

        # Simulate EscalationAgent handoff
        # In a real scenario, this would notify a human coach system.
        return HandoffResponse(
            user_id=user_id,
            status="success",
            message="Request for human coach received. An expert will contact you shortly.",
            handoff_type="escalation_agent",
            expert_contact="coach@example.com" # Example contact
        )
    except Exception as e:
        print(f"Error requesting human coach for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/consult_nutrition_expert", response_model=HandoffResponse)
async def consult_nutrition_expert(request: HandoffRequest):
    try:
        user_id = request.user_id
        if user_id not in user_sessions:
            pass # Allow without full session

        # Simulate NutritionExpertAgent handoff
        return HandoffResponse(
            user_id=user_id,
            status="success",
            message="Request for nutrition expert received. An expert will review your case.",
            handoff_type="nutrition_expert_agent",
            expert_contact="nutrition@example.com"
        )
    except Exception as e:
        print(f"Error consulting nutrition expert for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/consult_injury_expert", response_model=HandoffResponse)
async def consult_injury_expert(request: HandoffRequest):
    try:
        user_id = request.user_id
        if user_id not in user_sessions:
            pass # Allow without full session

        # Simulate InjurySupportAgent handoff
        return HandoffResponse(
            user_id=user_id,
            status="success",
            message="Request for injury support expert received. An expert will provide guidance.",
            handoff_type="injury_support_agent",
            expert_contact="injury@example.com"
        )
    except Exception as e:
        print(f"Error consulting injury expert for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# --- Mazeed Ahem Points (Further Important Considerations) ---

# 1. State Management:
#    `user_sessions` dictionary is used for in-memory state management.
#    For production, replace this with a persistent storage solution (e.g., database, Redis)
#    to ensure data durability and scalability across multiple API instances.

# 2. Error Handling:
#    Implemented with `try-except` blocks and `HTTPException` for graceful error responses.
#    Consider more specific exception handling and custom error classes for different scenarios.

# 3. Asynchronous Operations:
#    The endpoint `set_user_goal` is an `async def` function. If your actual agent's tools
#    (e.g., LLM calls, external API requests) involve I/O-bound operations, ensure they are
#    implemented asynchronously and awaited properly within the agent's logic to prevent blocking
#    the FastAPI event loop.

# 4. Security:
#    This example does NOT include any security measures (authentication, authorization, rate limiting).
#    For a production API, robust security is CRITICAL. Implement appropriate authentication
#    (e.g., OAuth2, API Keys) and authorization mechanisms.

# 5. Modularity:
#    For APIs with many endpoints, consider using `fastapi.APIRouter` to organize your routes
#    into separate modules for better maintainability and scalability.

# 6. Agent Implementation Details:
#    The current implementation simulates the agent's tool orchestration. In a real scenario,
#    you would likely have a method within `HealthWellnessAgent` that takes the `UserSessionContext`
#    and processes the request, internally calling `GoalAnalyzerTool`, `MealPlannerTool`, etc.,
#    and then updating the context. This would keep the FastAPI endpoint cleaner.
