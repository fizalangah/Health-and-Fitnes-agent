# Health & Wellness Planner Agent — Assignment Document  
Using OpenAI Agents SDK

---

## 🔹 Overview
This assignment focuses on building an AI-powered Health & Wellness Planner Agent using the OpenAI Agents SDK. The system should act as a digital wellness assistant capable of understanding user goals, guiding them through multi-step health planning, and offering personalized recommendations.

The agent should be able to:

- Collect user fitness and dietary goals through multi-turn conversation  
- Analyze goals and produce structured health plans  
- Maintain state and context across interactions  
- Stream responses in real time  
- Apply guardrails for valid input and structured output  
- Delegate tasks to specialized agents when needed  
- (Optional) Use lifecycle hooks for logging and tracking

The goal is to simulate a complete real-world AI wellness assistant that manages dynamic inputs, workflows, and decision-making.

---

## 💪 Project Objective

- Understand user health goals  
- Generate customized meals and workout plans  
- Track progress and schedule reminders  
- Provide real-time streaming interaction  
- Delegate to specialized agents when appropriate  

---

## ✅ SDK Features Overview

| Feature | Requirement |
|--------|-------------|
| Agent + Tool Creation | ✅ Required |
| State Management | ✅ Required |
| Guardrails (Input/Output) | ✅ Required |
| Real-Time Streaming | ✅ Required |
| Handoff to Another Agent | ✅ Required |
| Lifecycle Hooks | ✅ Optional |

---

## 🔧 Tools

| Tool Name | Purpose |
|-----------|---------|
| **GoalAnalyzerTool** | Converts user goals into structured format using guardrails |
| **MealPlannerTool** | Async tool generating 7-day meal plans based on preferences |
| **WorkoutRecommenderTool** | Recommends workout plan from parsed goals |
| **CheckinSchedulerTool** | Schedules weekly progress check-ins |
| **ProgressTrackerTool** | Tracks updates, progress logs, and modifies session context |

---

## 🤝 Handoffs (Specialized Agents)

Specialized agents are triggered via `handoff()` when certain conditions appear.

| Agent Name | Trigger Condition |
|------------|------------------|
| **EscalationAgent** | When the user wants a human coach |
| **NutritionExpertAgent** | Complex dietary needs (e.g., diabetes, allergies) |
| **InjurySupportAgent** | Injury-related or physical limitation concerns |

Each of these should be added in the `handoffs` parameter of the main agent and may implement `on_handoff()` for logging or setup.

---

## 📦 Context Management

Define a shared context class:

```python
class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[dict] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[dict] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[Dict[str, str]] = []
