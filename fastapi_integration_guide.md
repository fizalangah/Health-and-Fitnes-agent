# Agent ko FastAPI API main Integrate Karnay ka Tareeka

Iss guide main hum dekhain gay kay kaisay aap apnay maujooda agent ko FastAPI framework ka istemal kartay huay aik API main tabdeel kar saktay hain. Yeh aapko apnay agent ki functionality ko dosri applications ya front-end say connect karnay main madad day ga.

## Steps:

### Step 1: FastAPI Project Set Up Karna

Sab say pehlay, aapko apnay project main FastAPI aur Uvicorn install karna hoga (agar pehlay say nahi kiya hai). Uvicorn aik ASGI server hai jo FastAPI applications ko run karta hai.

```bash
pip install fastapi uvicorn
```

Apnay project root directory main `api.py` (ya koi aur suitable name) ki aik nayyi file banao.

### Step 2: Agent aur Context Classes Import Karna

Jo agent classes aur context classes aapnay banai hain, unko nayyi `api.py` file main import karain. Misal kay tor par, aapko `agents01.main_agent` say `MainAgent` aur `context.py` say `UserSessionContext` import karna hoga.

```python
# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Apnay agent aur context classes ko yahan import karain
# Misal kay tor par:
from agents01.main_agent import MainAgent
from context import UserSessionContext
# Agar aap kay tools alag files main hain to unko bhi import karain agar direct use karna ho
# from tools.goal_analyzer_tool import GoalAnalyzerTool
# ... aur bhi tools
```

### Step 3: FastAPI Application Initialize Karna

`api.py` file main FastAPI application ko initialize karain:

```python
# api.py (continue)

app = FastAPI()

# Agent ko initialize karain (aap isko global level par ya dependency injection kay through kar saktay hain)
# Production main isko theek tareeqay say manage karna hoga (e.g., singleton pattern)
main_agent_instance = MainAgent() # Ya jo bhi aap kay main agent ko initialize karnay ka tareeka hai
```

### Step 4: Pydantic Models Define Karna (API Request/Response Data)

API requests aur responses kay structure ko define karnay kay liye Pydantic models ka istemal karain. Yeh data validation aur documentation main madad karta hai. Misal kay tor par, agar aap goal set karnay kay liye API banana chahtay hain:

```python
# api.py (continue)

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
```

### Step 5: API Endpoints Banana

Ab aap `FastAPI` kay decorators ka istemal kartay huay API endpoints define karain gay. Har endpoint aik specific agent functionality ko expose karay ga.

```python
# api.py (continue)

@app.post("/set_goal")
async def set_user_goal(request: GoalRequest):
    try:
        # Yahan aap apnay agent ki logic ko call karain gay
        # Misal kay tor par, MainAgent ko GoalAnalyzerTool use karnay ko kahain
        # (Assuming MainAgent has a method to process goals)

        # Ye aik simplified example hai, asal implementation aapkay agent structure par munhasir hogi
        # Aapko agent kay andar tools ko call karnay ka mechanism banana hoga.

        # For demonstration purposes, let's assume MainAgent has a method like process_user_request
        # that takes context and a prompt, and returns updated context or a plan.

        # Temporarily create a context for this request if your agent needs it
        user_context = UserSessionContext(
            name=request.user_name,
            uid=hash(request.user_id) % (10**8), # Simple UID generation for example
            goal={"description": request.goal_description},
            diet_preferences=request.diet_preferences
        )
        
        # Ab yahan main_agent_instance.process_user_goal() ya is jaisa koi method call hoga
        # Jo GoalAnalyzerTool aur MealPlannerTool wagaira ko use karay ga.
        # Filhal, hum dummy response return kar rahay hain.
        
        # Agar aapka MainAgent asynchronosly tools call karta hai, to await use karain.
        # updated_context = await main_agent_instance.process_user_goal(user_context)

        # Dummy response
        meal_plan_example = [
            "Monday: Chicken Salad",
            "Tuesday: Lentil Soup",
            "Wednesday: Fish and Vegetables",
            "Thursday: Tofu Stir-fry",
            "Friday: Steak with Sweet Potato",
            "Saturday: Omelette and Fruits",
            "Sunday: Roast Chicken"
        ]
        workout_plan_example = {
            "Monday": "Strength Training (Upper Body)",
            "Tuesday": "Cardio (Running 30 min)",
            "Wednesday": "Strength Training (Lower Body)",
            "Thursday": "Yoga",
            "Friday": "Full Body HIIT",
            "Saturday": "Rest/Active Recovery",
            "Sunday": "Rest"
        }


        return PlanResponse(
            user_id=request.user_id,
            status="success",
            message="Goals processed and plans generated.",
            meal_plan=meal_plan_example,
            workout_plan=workout_plan_example
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Aap isi tarah dosray tools (e.g., /track_progress, /schedule_checkin) kay liye bhi endpoints bana saktay hain.
```

### Step 6: FastAPI Application Run Karna

Apni `api.py` file ko terminal main uvicorn ka istemal kartay huay run karain:

```bash
uvicorn api:app --reload
```

*   `api`: aapki Python file ka naam hai (jahan `app` object defined hai).
*   `app`: aapkay FastAPI application instance ka naam hai.
*   `--reload`: yeh option development kay doran code changes par server ko automatically reload kar deta hai.

Server run honay kay baad, aap browser main `http://127.0.0.1:8000/docs` par ja kar apni API ki interactive documentation (Swagger UI) dekh saktay hain. Yahan aap apnay endpoints ko test bhi kar saktay hain.

### Mazeed Ahem Points:

*   **State Management**: Agar aapka agent session-based state maintain karta hai (jaisa kay `UserSessionContext` say lagta hai), to aapko har user session kay liye alag context instance banana aur manage karna hoga. Yeh "Dependency Injection" ya request-specific context objects kay through kiya ja sakta hai.
*   **Error Handling**: Har endpoint main robust error handling (try-except blocks) ka istemal karain takay API graceful tareeqay say fail ho.
*   **Asynchronous Operations**: Aapkay tools shayad network requests (e.g., LLM calls) ya time-consuming operations kartay hon gay. FastAPI `async def` functions ko support karta hai, isliye apnay agent ki methods ko `await`able banayain jahan zaroori ho.
*   **Security**: Production deployments kay liye, API security (authentication, authorization, rate limiting) par tawajjo dain.
*   **Modularity**: Agar aapkay paas bohat saray agents aur tools hain, to `APIRouter` ka istemal kar kay apni API ko modules main organize karain.

Yeh guide aapko aik bunyadi shuruaat day gi. Aapko apnay specific agent ki implementation aur zarooriyat kay mutabiq adjustments karna hon gi.