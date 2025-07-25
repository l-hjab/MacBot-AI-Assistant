"""
Llama API Client for Macadamia Farming Chatbot
==============================================

This module handles communication with the Llama API for natural language
processing and response generation.
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LlamaClient:
    """
    Client for interacting with Llama API via Together AI
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Llama API client
        
        Args:
            api_key: Together AI API key (if not provided, will use environment variable)
        """
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY", "")
        self.api_url = "https://api.together.xyz/v1/chat/completions"
        self.model = "meta-llama/Llama-2-7b-chat-hf"
        self.max_tokens = 500
        self.temperature = 0.7
        
        if not self.api_key:
            logger.warning("No API key provided. Llama API functionality will be limited.")
    
    def generate_farming_response(self, 
                                user_query: str,
                                context: Dict[str, Any] = None,
                                farming_domain: str = "general") -> Dict[str, Any]:
        """
        Generate a farming advice response using Llama API
        
        Args:
            user_query: User's question or request
            context: Additional context (predictions, farm data, etc.)
            farming_domain: Specific farming domain (planting, pest, fertilizer, etc.)
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Build system prompt based on farming domain
            system_prompt = self._build_system_prompt(farming_domain, context)
            
            # Build user message with context
            user_message = self._build_user_message(user_query, context)
            
            # Make API call
            response = self._call_llama_api(system_prompt, user_message)
            
            if response['success']:
                return {
                    'success': True,
                    'response': response['content'],
                    'domain': farming_domain,
                    'timestamp': datetime.now().isoformat(),
                    'model_used': self.model
                }
            else:
                return self._fallback_response(user_query, farming_domain)
                
        except Exception as e:
            logger.error(f"Error generating farming response: {e}")
            return self._fallback_response(user_query, farming_domain)
    
    def _build_system_prompt(self, domain: str, context: Dict[str, Any] = None) -> str:
        """Build system prompt based on farming domain"""
        
        base_prompt = """You are an expert macadamia farming advisor with deep knowledge of organic farming practices. 
You provide practical, actionable advice to farmers in a friendly and easy-to-understand manner. 
Always prioritize organic and sustainable farming methods."""
        
        domain_prompts = {
            "planting": """
Focus on macadamia planting advice including:
- Site selection and soil preparation
- Optimal planting times and spacing
- Tree variety selection
- Early care and establishment
- Organic soil amendments
""",
            "pest_management": """
Focus on organic pest management for macadamia trees including:
- Pest identification and monitoring
- Organic treatment options
- Integrated pest management strategies
- Beneficial insect conservation
- Prevention methods
""",
            "fertilization": """
Focus on organic fertilization for macadamia trees including:
- Organic fertilizer recommendations
- Soil testing and nutrient management
- Composting and organic amendments
- Foliar feeding programs
- Seasonal fertilization schedules
""",
            "harvesting": """
Focus on macadamia harvesting including:
- Harvest timing and maturity indicators
- Harvesting methods and equipment
- Post-harvest handling and processing
- Quality assessment and grading
- Storage recommendations
""",
            "certification": """
Focus on organic certification for macadamia farming including:
- Certification requirements and process
- Record keeping and documentation
- Approved organic inputs
- Transition period management
- Maintaining certification compliance
"""
        }
        
        domain_specific = domain_prompts.get(domain, "")
        
        # Add context information if available
        context_info = ""
        if context:
            if 'predictions' in context:
                context_info += f"\nCurrent predictions: {context['predictions']}"
            if 'farm_conditions' in context:
                context_info += f"\nFarm conditions: {context['farm_conditions']}"
            if 'season' in context:
                context_info += f"\nCurrent season: {context['season']}"
        
        return f"{base_prompt}\n{domain_specific}\n{context_info}\n\nProvide helpful, practical advice in a conversational tone."
    
    def _build_user_message(self, query: str, context: Dict[str, Any] = None) -> str:
        """Build user message with context"""
        message = query
        
        if context and 'farm_data' in context:
            farm_data = context['farm_data']
            message += f"\n\nMy farm details: {farm_data}"
        
        return message
    
    def _call_llama_api(self, system_prompt: str, user_message: str) -> Dict[str, Any]:
        """Make API call to Llama"""
        if not self.api_key:
            return {'success': False, 'error': 'No API key available'}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return {'success': True, 'content': content}
            else:
                logger.error(f"API call failed with status {response.status_code}: {response.text}")
                return {'success': False, 'error': f'API error: {response.status_code}'}
                
        except Exception as e:
            logger.error(f"API call exception: {e}")
            return {'success': False, 'error': str(e)}
    
    def _fallback_response(self, query: str, domain: str) -> Dict[str, Any]:
        """Generate fallback response when API is unavailable"""
        
        fallback_responses = {
            "planting": """For macadamia planting, I recommend:
1. Choose well-draining soil with pH 6.0-6.5
2. Plant in spring after last frost or autumn before first frost
3. Space trees 8m x 8m for good air circulation
4. Prepare planting holes with compost and organic matter
5. Water regularly during establishment period

For specific variety recommendations and detailed planting guides, consult your local agricultural extension office.""",
            
            "pest_management": """For organic pest management:
1. Regular monitoring is key - inspect trees weekly
2. Use pheromone traps for early pest detection
3. Encourage beneficial insects with diverse plantings
4. Apply neem oil or insecticidal soap for soft-bodied pests
5. Maintain good orchard sanitation

For severe pest issues, consider consulting an organic farming specialist.""",
            
            "fertilization": """For organic fertilization:
1. Test soil annually to determine nutrient needs
2. Apply compost in spring and autumn (10-20kg per mature tree)
3. Use organic fertilizers like blood meal, bone meal, and kelp meal
4. Consider foliar feeding with fish emulsion during growing season
5. Maintain soil pH between 6.0-6.5

Adjust fertilization based on tree age and soil test results.""",
            
            "harvesting": """For macadamia harvesting:
1. Harvest when nuts fall naturally from trees
2. Collect nuts within 2-3 days to maintain quality
3. Remove husks promptly after collection
4. Dry nuts to 1.5-3.5% moisture content
5. Store in cool, dry conditions with good ventilation

Proper timing and handling are crucial for nut quality.""",
            
            "certification": """For organic certification:
1. Choose an accredited certification body
2. Maintain detailed records of all inputs and practices
3. Allow 3-year transition period from conventional farming
4. Use only approved organic inputs
5. Undergo annual inspections

Start record-keeping immediately, even before formal certification begins."""
        }
        
        default_response = """I'd be happy to help with your macadamia farming question! 
For the most accurate and up-to-date advice, I recommend:
1. Consulting your local agricultural extension office
2. Connecting with other organic macadamia farmers in your area
3. Reviewing organic farming resources and publications
4. Considering soil and plant tissue testing for specific recommendations

Feel free to ask more specific questions about macadamia farming practices!"""
        
        response_text = fallback_responses.get(domain, default_response)
        
        return {
            'success': True,
            'response': response_text,
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'model_used': 'fallback',
            'note': 'Fallback response - API unavailable'
        }
    
    def summarize_predictions(self, predictions: Dict[str, Any]) -> str:
        """
        Summarize ML predictions in natural language
        
        Args:
            predictions: Dictionary of model predictions
            
        Returns:
            Natural language summary of predictions
        """
        try:
            summary_parts = []
            
            if 'pest_risk' in predictions:
                risk_level = predictions['pest_risk'].get('overall_risk_level', 'unknown')
                summary_parts.append(f"Pest risk is currently {risk_level}")
            
            if 'fertilizer_need' in predictions:
                fert_need = predictions['fertilizer_need']
                summary_parts.append(f"Fertilizer need is {fert_need}")
            
            if 'harvest_ready' in predictions:
                harvest = predictions['harvest_ready']
                if harvest:
                    summary_parts.append("Trees appear ready for harvest")
                else:
                    summary_parts.append("Trees are not yet ready for harvest")
            
            if 'yield_prediction' in predictions:
                yield_pred = predictions['yield_prediction']
                summary_parts.append(f"Expected yield is approximately {yield_pred:.1f} kg per tree")
            
            if summary_parts:
                return "Based on current conditions: " + ", ".join(summary_parts) + "."
            else:
                return "Current farm analysis is being processed."
                
        except Exception as e:
            logger.error(f"Error summarizing predictions: {e}")
            return "Farm condition analysis is available upon request."
    
    def explain_recommendation(self, recommendation: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get detailed explanation for a farming recommendation
        
        Args:
            recommendation: The recommendation to explain
            context: Additional context for the explanation
            
        Returns:
            Detailed explanation response
        """
        system_prompt = """You are an expert macadamia farming advisor. 
Provide detailed, educational explanations for farming recommendations. 
Explain the science behind the advice and include practical implementation tips."""
        
        user_message = f"Please explain this macadamia farming recommendation in detail: {recommendation}"
        
        if context:
            user_message += f"\nContext: {json.dumps(context, indent=2)}"
        
        response = self._call_llama_api(system_prompt, user_message)
        
        if response['success']:
            return {
                'success': True,
                'explanation': response['content'],
                'recommendation': recommendation,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'success': True,
                'explanation': f"This recommendation ({recommendation}) is based on established macadamia farming best practices. For detailed scientific explanations, consult agricultural research publications or extension resources.",
                'recommendation': recommendation,
                'timestamp': datetime.now().isoformat(),
                'note': 'Fallback explanation'
            }

