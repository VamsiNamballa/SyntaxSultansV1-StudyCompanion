from .agent import Agent, Plan
from .context import Context
from .context import BotMessage
from .genai import ask_genai  # Importing GenAI handler

class BotBrain(Agent):
    """
    BotBrain logic:
    - First attempts rule-based response matching (SimpleBrain)
    - If no rule matches, falls back to Hugging Face GenAI with a refined prompt.
    """
    def __init__(self, id):
        self.debug = False
        self.announcement = None
        super().__init__(id)

    def process(self, context: BotMessage):
        """
        Extended process method:
        1. Try rule-based matching first
        2. Fallback to GenAI if no good response
        """
        # (1) Call parent processing (SimpleBrain rule matching)
        super().process(context=context)
        
        # (2) If no valid rule-based response found, fallback to GenAI
        if (not context.response) or (context.response.strip() == "") or (context.response.strip().lower() == "i have no idea how to respond!"):
            user_message = context.facts.get("message", "")
            if self.debug:
                print("[BotBrain] No rule matched or bad response. Falling back to GenAI.")
            # Refine the GenAI prompt to ensure larger, tutor-like responses
            refined_prompt = f"As a tutor, explain the following concept in detail, with examples and easy-to-understand explanations:\n{user_message}"
            context.response = ask_genai(refined_prompt)  # Pass the refined prompt to GenAI
