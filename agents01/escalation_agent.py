from agents import Agent

class EscalationAgent(Agent):
    name: str = "EscalationAgent"

    description: str = (
        "Handles situations where the user requests to speak with a human coach "
        "or needs support beyond automated capabilities."
    )

    base_instructions: str = (
        "Your primary role is to acknowledge the user's request for human intervention "
        "and provide a reassuring message that their request has been noted. "
        "Explain that a human coach will contact the user soon. "
        "You do not perform any coaching yourself — you only facilitate the handoff."
    )

    tools = []

    def __init__(self):
        super().__init__(
            name=self.name,
            instructions=f"{self.description}\n\n{self.base_instructions}",
            tools=self.tools,
        )
