"""
Macadamia Farming AI Chatbot
============================

An AI-powered chatbot that provides comprehensive organic farming advice 
for macadamia farmers, covering planting, pest management, fertilization, 
harvesting, and certification guidance.

Features:
- Random Forest models for farming predictions
- Llama API integration for natural language responses
- Comprehensive farming knowledge base
- User-friendly Streamlit interface
"""

__version__ = "1.0.0"
__author__ = "Macadamia Farming AI Team"

from .core.chatbot import MacadamiaBot
from .core.query_classifier import QueryClassifier
from .core.response_generator import ResponseGenerator

__all__ = [
    "MacadamiaBot",
    "QueryClassifier", 
    "ResponseGenerator"
]

