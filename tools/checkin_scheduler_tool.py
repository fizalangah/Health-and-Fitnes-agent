from typing import Optional, Type
import datetime
from agents import function_tool

@function_tool(
    name_override="CheckinSchedulerTool",
    description_override="Schedules weekly progress check-ins for the user. This tool allows setting up recurring reminders or events for tracking health and wellness progress.",
)
async def CheckinSchedulerTool(user_id: int, checkin_day: str, checkin_time: str, reminder_type: Optional[str] = "email") -> dict:
    """
    Schedules weekly progress check-ins for the user.
    This tool allows setting up recurring reminders or events for tracking health and wellness progress.
    """
    # In a real system, this would integrate with a calendar API or a notification service.
    # For this prototype, we'll simulate the scheduling and return a confirmation.

    days_of_week = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
        "Friday": 4, "Saturday": 5, "Sunday": 6
    }

    today = datetime.date.today()
    current_day_of_week = today.weekday() # Monday is 0, Sunday is 6
    
    target_day_of_week = days_of_week.get(checkin_day.capitalize())

    if target_day_of_week is None:
        return {
            "scheduled": False,
            "message": f"Invalid check-in day: {checkin_day}. Please provide a valid day of the week.",
            "next_checkin_date": None
        }

    days_until_next_checkin = (target_day_of_week - current_day_of_week + 7) % 7
    if days_until_next_checkin == 0 and datetime.datetime.now().strftime("%H:%M") > checkin_time.replace(" AM", "").replace(" PM", "")[:5]:
        # If target day is today, but time has passed, schedule for next week
        days_until_next_checkin += 7
        
    next_checkin_date = today + datetime.timedelta(days=days_until_next_checkin)
    
    message = (f"Weekly check-in scheduled for user {user_id} every {checkin_day} at {checkin_time} "
                f"via {reminder_type}. Your next check-in is on {next_checkin_date.strftime('%Y-%m-%d')}.")
    
    return {
        "scheduled": True,
        "message": message,
        "next_checkin_date": next_checkin_date.strftime('%Y-%m-%d')
    }