from agents import Agent

class InjurySupportAgent(Agent):
    name: str = "InjurySupportAgent"

    description: str = (
        "Offers guidance for users with injuries or physical limitations, "
        "focusing on safe exercise and recovery."
    )

    base_instructions: str = (
        "Your task is to provide supportive and cautious advice related to physical "
        "activity when the user has an injury. Ask about the injury type, severity, "
        "and any medical advice received. Suggest safe modifications, rest guidance, "
        "and when to seek professional medical care. Safety must always come first."
    )

    tools = []

    def __init__(self):
        super().__init__(
            name=self.name,
            instructions=f"{self.description}\n\n{self.base_instructions}",
            tools=self.tools,
        )
