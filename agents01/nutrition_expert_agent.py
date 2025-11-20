from agents import Agent

class NutritionExpertAgent(Agent):
    name: str = "NutritionExpertAgent"

    description: str = (
        "Provides specialized dietary advice for complex needs such as diabetes, "
        "allergies, or specific health conditions."
    )

    base_instructions: str = (
        "Your role is to offer detailed and safe nutritional guidance. "
        "Ask clarifying questions about the user’s conditions, diet, and medications. "
        "Provide evidence-based recommendations for foods and meal planning. "
        "You must always remind the user to consult a healthcare professional "
        "for medical or clinical advice."
    )

    tools = []

    def __init__(self):
        super().__init__(
            name=self.name,
            instructions=f"{self.description}\n\n{self.base_instructions}",
            tools=self.tools,
        )
