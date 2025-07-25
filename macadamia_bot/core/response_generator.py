"""
Response Generator Module
==========================

Handles generating natural language responses for the Macadamia Farming AI Chatbot.
Integrates with Llama API (or other models) to provide informative and helpful replies.
"""

class ResponseGenerator:
    def __init__(self, model=None):
        """
        Initialize the ResponseGenerator.

        Parameters:
        - model: an optional language model instance (e.g., Llama API wrapper)
        """
        self.model = model

    def generate(self, query: str) -> str:
        """
        Generate a response based on the user query.

        Parameters:
        - query (str): The user's input question.

        Returns:
        - str: The AI-generated response.
        """
        if self.model:
            # Example: use the external Llama API or your model here
            response = self.model.generate_text(query)
        else:
            # Fallback dummy response
            response = f"I'm here to help with macadamia farming questions! You asked: '{query}'."

        return response
