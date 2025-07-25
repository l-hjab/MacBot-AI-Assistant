"""
Main Macadamia Farming Chatbot
==============================

This is the core chatbot class that orchestrates all components to provide
comprehensive farming advice to macadamia farmers.
"""

import json
import os
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from .query_classifier import QueryClassifier
from .llama_client import LlamaClient
from ..models.pest_predictor import PestRiskPredictor
from ..domains.planting import PlantingAdvisor
from ..domains.pest_management import PestManagementAdvisor
from ..domains.fertilization import FertilizationAdvisor
from ..domains.harvesting import HarvestingAdvisor
from ..domains.certification import CertificationAdvisor

logger = logging.getLogger(__name__)

class MacadamiaBot:
    """
    Main chatbot class for macadamia farming advice
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the macadamia farming chatbot
        
        Args:
            api_key: Together AI API key for Llama integration
        """
        self.query_classifier = QueryClassifier()
        self.llama_client = LlamaClient(api_key)
        
        # Initialize domain advisors
        self.domain_advisors = {
            'planting': PlantingAdvisor(),
            'pest_management': PestManagementAdvisor(),
            'fertilization': FertilizationAdvisor(),
            'harvesting': HarvestingAdvisor(),
            'certification': CertificationAdvisor()
        }
        
        # Initialize ML predictors
        try:
            self.pest_predictor = PestRiskPredictor()
        except Exception as e:
            logger.warning(f"Could not initialize pest predictor: {e}")
            self.pest_predictor = None
        
        # Conversation history
        self.conversation_history = []
        
        logger.info("MacadamiaBot initialized successfully")
    
    def chat(self, 
             user_input: str, 
             farm_data: Optional[Dict[str, Any]] = None,
             user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Main chat interface for the bot
        
        Args:
            user_input: User's message/question
            farm_data: Optional farm-specific data for predictions
            user_id: Optional user identifier for conversation tracking
            
        Returns:
            Comprehensive response with advice, predictions, and recommendations
        """
        try:
            # Classify the user query
            classification = self.query_classifier.classify_query(user_input, farm_data)
            
            # Generate response based on classification
            response = self._generate_response(user_input, classification, farm_data)
            
            # Add to conversation history
            self._update_conversation_history(user_input, response, user_id)
            
            # Add helpful follow-up suggestions
            response['followup_questions'] = self.query_classifier.get_followup_questions(classification)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat processing: {e}")
            return self._error_response(user_input)
    
    def _generate_response(self, 
                          user_input: str, 
                          classification: Dict[str, Any],
                          farm_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate comprehensive response based on query classification"""
        
        domain = classification['domain']
        strategy = classification['response_strategy']
        
        response = {
            'user_query': user_input,
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'response_components': {}
        }
        
        # Get ML predictions if needed
        if strategy['use_ml_predictions'] and farm_data:
            predictions = self._get_ml_predictions(
                strategy['prediction_types'], 
                farm_data
            )
            response['response_components']['predictions'] = predictions
        
        # Get domain-specific advice
        if domain in self.domain_advisors:
            domain_advice = self.domain_advisors[domain].get_advice(
                user_input, 
                classification['parameters'],
                farm_data
            )
            response['response_components']['domain_advice'] = domain_advice
        
        # Generate conversational response
        conversational_response = self._get_conversational_response(
            user_input, 
            classification, 
            response['response_components'],
            farm_data
        )
        response['response_components']['conversational'] = conversational_response
        
        # Combine all components into final response
        response['final_response'] = self._combine_response_components(
            response['response_components'],
            classification
        )
        
        return response
    
    def _get_ml_predictions(self, 
                           prediction_types: List[str], 
                           farm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get ML model predictions"""
        predictions = {}
        
        # Extract required parameters from farm data
        required_params = [
            'soil_ph', 'temperature', 'humidity', 
            'rainfall', 'season', 'tree_age'
        ]
        
        # Check if we have all required parameters
        if not all(param in farm_data for param in required_params):
            return {
                'error': 'Insufficient farm data for predictions',
                'required_parameters': required_params,
                'provided_parameters': list(farm_data.keys())
            }
        
        # Pest risk prediction
        if 'pest_risk' in prediction_types and self.pest_predictor:
            try:
                pest_prediction = self.pest_predictor.predict_pest_risk(
                    soil_ph=farm_data['soil_ph'],
                    temperature=farm_data['temperature'],
                    humidity=farm_data['humidity'],
                    rainfall=farm_data['rainfall'],
                    season=farm_data['season'],
                    tree_age=farm_data['tree_age']
                )
                predictions['pest_risk'] = pest_prediction
            except Exception as e:
                logger.error(f"Pest prediction error: {e}")
                predictions['pest_risk'] = {'error': str(e)}
        
        # Add other prediction types here as models become available
        # fertilizer_need, harvest_timing, yield_prediction
        
        return predictions
    
    def _get_conversational_response(self, 
                                   user_input: str,
                                   classification: Dict[str, Any],
                                   response_components: Dict[str, Any],
                                   farm_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate conversational AI response"""
        
        # Build context for Llama API
        context = {
            'classification': classification,
            'farm_data': farm_data,
            'predictions': response_components.get('predictions'),
            'domain_advice': response_components.get('domain_advice')
        }
        
        # Generate response using Llama API
        llama_response = self.llama_client.generate_farming_response(
            user_input,
            context,
            classification['domain']
        )
        
        return llama_response
    
    def _combine_response_components(self, 
                                   components: Dict[str, Any],
                                   classification: Dict[str, Any]) -> str:
        """Combine all response components into a coherent final response"""
        
        response_parts = []
        
        # Start with conversational response if available
        if 'conversational' in components and components['conversational']['success']:
            response_parts.append(components['conversational']['response'])
        
        # Add prediction results if available
        if 'predictions' in components:
            predictions = components['predictions']
            if 'pest_risk' in predictions and 'error' not in predictions['pest_risk']:
                pest_info = predictions['pest_risk']
                response_parts.append(
                    f"\n🔍 **Current Pest Risk Analysis:**\n"
                    f"Risk Level: {pest_info['overall_risk_level'].title()}\n"
                    f"Confidence: {pest_info['confidence']:.0%}"
                )
                
                if pest_info.get('recommendations'):
                    response_parts.append(
                        f"\n📋 **Immediate Recommendations:**\n" +
                        "\n".join(f"• {rec}" for rec in pest_info['recommendations'][:3])
                    )
        
        # Add domain-specific advice if available
        if 'domain_advice' in components:
            domain_advice = components['domain_advice']
            if isinstance(domain_advice, dict) and 'advice' in domain_advice:
                response_parts.append(f"\n💡 **Expert Advice:**\n{domain_advice['advice']}")
        
        # Combine all parts
        if response_parts:
            return "\n".join(response_parts)
        else:
            return self._fallback_response(classification['domain'])
    
    def _fallback_response(self, domain: str) -> str:
        """Generate fallback response when other methods fail"""
        
        fallback_responses = {
            'planting': "For macadamia planting advice, I recommend focusing on site selection with well-draining soil, proper spacing (8m x 8m), and choosing appropriate varieties for your climate. Would you like specific guidance on any of these aspects?",
            
            'pest_management': "For pest management, regular monitoring is key. Check your trees weekly for signs of pests like nut borers or stink bugs. Organic treatments like neem oil and beneficial insects can be very effective. What specific pest concerns do you have?",
            
            'fertilization': "Macadamia trees benefit from organic fertilization with compost, aged manure, and balanced organic fertilizers. Soil testing annually helps determine specific nutrient needs. What's your current fertilization program?",
            
            'harvesting': "Harvest timing is crucial for nut quality. Wait for nuts to fall naturally, collect within 2-3 days, and process promptly. Proper drying to 1.5-3.5% moisture is essential. What stage of harvest are you at?",
            
            'certification': "Organic certification requires 3-year transition period, detailed record keeping, and use of approved inputs only. Start documenting everything now, even before formal certification begins. Which certification are you pursuing?",
            
            'general': "I'm here to help with all aspects of macadamia farming! I can provide advice on planting, pest management, fertilization, harvesting, and organic certification. What specific area would you like to discuss?"
        }
        
        return fallback_responses.get(domain, fallback_responses['general'])
    
    def _update_conversation_history(self, 
                                   user_input: str, 
                                   response: Dict[str, Any],
                                   user_id: Optional[str] = None):
        """Update conversation history"""
        
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'user_input': user_input,
            'domain': response.get('domain'),
            'response_summary': response.get('final_response', '')[:200] + '...'
        }
        
        self.conversation_history.append(history_entry)
        
        # Keep only last 50 conversations to manage memory
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def _error_response(self, user_input: str) -> Dict[str, Any]:
        """Generate error response when processing fails"""
        
        return {
            'user_query': user_input,
            'domain': 'error',
            'timestamp': datetime.now().isoformat(),
            'final_response': """I apologize, but I encountered an error processing your request. 
            
Here are some general macadamia farming tips while I recover:
• Regular monitoring of trees is essential for healthy orchards
• Organic practices build long-term soil health and sustainability  
• Proper timing of farming activities greatly impacts success
• Local agricultural extension offices are excellent resources

Please try rephrasing your question, and I'll do my best to help!""",
            'error': True,
            'followup_questions': [
                "What specific aspect of macadamia farming interests you most?",
                "Are you dealing with any particular challenges in your orchard?",
                "Would you like general advice on organic macadamia farming?"
            ]
        }
    
    def get_farm_data_template(self) -> Dict[str, Any]:
        """
        Get template for farm data input
        
        Returns:
            Template dictionary showing required farm data structure
        """
        return {
            'soil_ph': 6.2,  # pH level (5.0-7.5)
            'temperature': 24,  # Current temperature in Celsius
            'humidity': 65,  # Relative humidity percentage
            'rainfall': 120,  # Recent rainfall in mm
            'season': 'spring',  # Current season
            'tree_age': 5,  # Age of trees in years
            'farm_location': 'optional',  # Geographic location
            'orchard_size': 'optional',  # Size in hectares
            'varieties': ['optional'],  # Macadamia varieties grown
            'farming_experience': 'optional'  # Years of experience
        }
    
    def get_conversation_summary(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get summary of conversation history
        
        Args:
            user_id: Optional user ID to filter conversations
            
        Returns:
            Summary of conversation history
        """
        if user_id:
            user_conversations = [
                conv for conv in self.conversation_history 
                if conv.get('user_id') == user_id
            ]
        else:
            user_conversations = self.conversation_history
        
        if not user_conversations:
            return {'message': 'No conversation history found'}
        
        # Analyze conversation patterns
        domains = [conv['domain'] for conv in user_conversations if conv.get('domain')]
        domain_counts = {}
        for domain in domains:
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        return {
            'total_conversations': len(user_conversations),
            'most_discussed_topics': domain_counts,
            'recent_conversations': user_conversations[-5:],  # Last 5 conversations
            'first_conversation': user_conversations[0]['timestamp'] if user_conversations else None,
            'last_conversation': user_conversations[-1]['timestamp'] if user_conversations else None
        }

