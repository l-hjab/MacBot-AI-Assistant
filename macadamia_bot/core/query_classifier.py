"""
Query Classification Module
===========================

This module classifies user queries to determine the appropriate response strategy
(ML prediction, knowledge base lookup, or conversational AI).
"""

import re
from typing import Dict, List, Tuple, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class QueryClassifier:
    """
    Classifies user queries to determine the best response approach
    """
    
    def __init__(self):
        """Initialize the query classifier"""
        self.domain_keywords = self._load_domain_keywords()
        self.intent_patterns = self._load_intent_patterns()
        self.prediction_triggers = self._load_prediction_triggers()
    
    def _load_domain_keywords(self) -> Dict[str, List[str]]:
        """Load keywords for different farming domains"""
        return {
            "planting": [
                "plant", "planting", "seed", "seedling", "transplant", "spacing", 
                "site selection", "soil preparation", "variety", "cultivar",
                "establishment", "when to plant", "how to plant", "planting time"
            ],
            "pest_management": [
                "pest", "insect", "bug", "borer", "scale", "stink bug", "aphid",
                "damage", "infestation", "spray", "treatment", "control",
                "organic pesticide", "beneficial insects", "IPM", "monitoring"
            ],
            "fertilization": [
                "fertilizer", "fertilize", "nutrition", "nutrient", "compost",
                "organic matter", "nitrogen", "phosphorus", "potassium",
                "soil test", "pH", "amendment", "feeding", "foliar"
            ],
            "harvesting": [
                "harvest", "harvesting", "picking", "collection", "maturity",
                "ripe", "ready", "timing", "when to harvest", "nut drop",
                "processing", "drying", "storage", "quality"
            ],
            "certification": [
                "organic", "certification", "certified", "standards", "inspection",
                "transition", "approved inputs", "record keeping", "compliance",
                "certifier", "OMRI", "USDA organic"
            ],
            "general": [
                "macadamia", "tree", "orchard", "farm", "farming", "growing",
                "care", "maintenance", "pruning", "irrigation", "water"
            ]
        }
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for different user intents"""
        return {
            "prediction_request": [
                r"predict", r"forecast", r"estimate", r"expect", r"likely",
                r"what will", r"how much", r"when will", r"should I",
                r"is it time", r"ready for", r"risk of"
            ],
            "advice_request": [
                r"how to", r"how do I", r"what should", r"recommend",
                r"best way", r"advice", r"suggest", r"help me",
                r"guide", r"tips"
            ],
            "information_request": [
                r"what is", r"what are", r"tell me about", r"explain",
                r"describe", r"information", r"learn about", r"understand"
            ],
            "problem_solving": [
                r"problem", r"issue", r"trouble", r"wrong", r"help",
                r"fix", r"solve", r"disease", r"dying", r"yellowing"
            ],
            "comparison_request": [
                r"compare", r"difference", r"better", r"versus", r"vs",
                r"which", r"choose", r"select", r"prefer"
            ]
        }
    
    def _load_prediction_triggers(self) -> Dict[str, List[str]]:
        """Load triggers that indicate ML prediction is needed"""
        return {
            "pest_risk": [
                "pest risk", "insect damage", "spray schedule", "pest forecast",
                "bug problem", "infestation risk", "pest pressure"
            ],
            "fertilizer_need": [
                "fertilizer need", "nutrient requirement", "feeding schedule",
                "fertilize now", "nutrition status", "soil fertility"
            ],
            "harvest_timing": [
                "harvest time", "ready to harvest", "harvest schedule",
                "maturity", "when to pick", "harvest forecast"
            ],
            "yield_prediction": [
                "yield estimate", "production forecast", "expected harvest",
                "crop yield", "how much yield", "production estimate"
            ]
        }
    
    def classify_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Classify a user query to determine response strategy
        
        Args:
            query: User's input query
            context: Additional context (farm data, previous conversation, etc.)
            
        Returns:
            Classification results with recommended response strategy
        """
        try:
            query_lower = query.lower()
            
            # Determine primary domain
            domain = self._classify_domain(query_lower)
            
            # Determine user intent
            intent = self._classify_intent(query_lower)
            
            # Check if ML prediction is needed
            prediction_needs = self._identify_prediction_needs(query_lower)
            
            # Determine response strategy
            response_strategy = self._determine_response_strategy(
                domain, intent, prediction_needs, context
            )
            
            # Extract any specific parameters from query
            parameters = self._extract_parameters(query_lower, domain)
            
            return {
                'domain': domain,
                'intent': intent,
                'prediction_needs': prediction_needs,
                'response_strategy': response_strategy,
                'parameters': parameters,
                'confidence': self._calculate_confidence(domain, intent, prediction_needs),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error classifying query: {e}")
            return self._fallback_classification()
    
    def _classify_domain(self, query: str) -> str:
        """Classify the farming domain of the query"""
        domain_scores = {}
        
        for domain, keywords in self.domain_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in query:
                    # Exact match gets higher score
                    if keyword == query.strip():
                        score += 3
                    # Phrase match gets medium score
                    elif len(keyword.split()) > 1:
                        score += 2
                    # Single word match gets base score
                    else:
                        score += 1
            domain_scores[domain] = score
        
        # Return domain with highest score, default to general
        if domain_scores:
            best_domain = max(domain_scores, key=domain_scores.get)
            if domain_scores[best_domain] > 0:
                return best_domain
        
        return "general"
    
    def _classify_intent(self, query: str) -> str:
        """Classify the user's intent"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return intent
        
        # Default intent based on query structure
        if "?" in query:
            return "information_request"
        elif any(word in query for word in ["help", "how", "what", "when", "where", "why"]):
            return "advice_request"
        else:
            return "general_inquiry"
    
    def _identify_prediction_needs(self, query: str) -> List[str]:
        """Identify what types of predictions might be needed"""
        needed_predictions = []
        
        for prediction_type, triggers in self.prediction_triggers.items():
            for trigger in triggers:
                if trigger in query:
                    needed_predictions.append(prediction_type)
                    break
        
        # Additional logic for implicit prediction needs
        if any(word in query for word in ["should i", "is it time", "when to"]):
            if "spray" in query or "treat" in query:
                needed_predictions.append("pest_risk")
            elif "fertilize" in query or "feed" in query:
                needed_predictions.append("fertilizer_need")
            elif "harvest" in query or "pick" in query:
                needed_predictions.append("harvest_timing")
        
        return list(set(needed_predictions))  # Remove duplicates
    
    def _determine_response_strategy(self, 
                                   domain: str, 
                                   intent: str, 
                                   prediction_needs: List[str],
                                   context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Determine the best response strategy"""
        
        strategy = {
            'primary_method': 'conversational',
            'use_ml_predictions': len(prediction_needs) > 0,
            'use_knowledge_base': True,
            'prediction_types': prediction_needs,
            'requires_farm_data': False
        }
        
        # If predictions are needed, prioritize ML approach
        if prediction_needs:
            strategy['primary_method'] = 'ml_prediction'
            strategy['requires_farm_data'] = True
        
        # For specific domains, always use knowledge base
        if domain in ['certification', 'planting']:
            strategy['use_knowledge_base'] = True
        
        # For problem-solving, combine all approaches
        if intent == 'problem_solving':
            strategy['primary_method'] = 'hybrid'
            strategy['use_ml_predictions'] = True
            strategy['use_knowledge_base'] = True
        
        # For comparison requests, use knowledge base primarily
        if intent == 'comparison_request':
            strategy['primary_method'] = 'knowledge_base'
        
        return strategy
    
    def _extract_parameters(self, query: str, domain: str) -> Dict[str, Any]:
        """Extract specific parameters from the query"""
        parameters = {}
        
        # Extract numbers (could be measurements, ages, etc.)
        numbers = re.findall(r'\d+\.?\d*', query)
        if numbers:
            parameters['numbers'] = [float(n) for n in numbers]
        
        # Extract seasons
        seasons = ['spring', 'summer', 'autumn', 'fall', 'winter']
        for season in seasons:
            if season in query:
                parameters['season'] = season
                break
        
        # Extract tree age indicators
        age_patterns = [r'(\d+)\s*year', r'young', r'mature', r'old']
        for pattern in age_patterns:
            match = re.search(pattern, query)
            if match:
                if match.group(0).isdigit():
                    parameters['tree_age'] = int(match.group(1))
                else:
                    parameters['tree_age_category'] = match.group(0)
                break
        
        # Extract specific varieties if mentioned
        varieties = ['beaumont', 'a4', 'a16', 'a38', 'own venture', 'daddow']
        for variety in varieties:
            if variety in query:
                parameters['variety'] = variety
                break
        
        # Extract urgency indicators
        urgency_words = ['urgent', 'emergency', 'immediate', 'asap', 'quickly']
        if any(word in query for word in urgency_words):
            parameters['urgency'] = 'high'
        
        return parameters
    
    def _calculate_confidence(self, domain: str, intent: str, prediction_needs: List[str]) -> float:
        """Calculate confidence score for the classification"""
        confidence = 0.5  # Base confidence
        
        # Higher confidence for specific domains
        if domain != 'general':
            confidence += 0.2
        
        # Higher confidence for clear intents
        if intent in ['prediction_request', 'advice_request', 'information_request']:
            confidence += 0.2
        
        # Higher confidence when prediction needs are identified
        if prediction_needs:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _fallback_classification(self) -> Dict[str, Any]:
        """Fallback classification when processing fails"""
        return {
            'domain': 'general',
            'intent': 'general_inquiry',
            'prediction_needs': [],
            'response_strategy': {
                'primary_method': 'conversational',
                'use_ml_predictions': False,
                'use_knowledge_base': True,
                'prediction_types': [],
                'requires_farm_data': False
            },
            'parameters': {},
            'confidence': 0.3,
            'timestamp': datetime.now().isoformat(),
            'note': 'Fallback classification used'
        }
    
    def get_followup_questions(self, classification: Dict[str, Any]) -> List[str]:
        """
        Generate relevant follow-up questions based on classification
        
        Args:
            classification: Query classification results
            
        Returns:
            List of suggested follow-up questions
        """
        domain = classification['domain']
        intent = classification['intent']
        
        followup_questions = {
            'planting': [
                "What's your soil type and pH level?",
                "Which macadamia variety are you considering?",
                "What's your local climate like?",
                "How large is your planting area?"
            ],
            'pest_management': [
                "What specific pest symptoms are you seeing?",
                "How old are your trees?",
                "What's the current weather been like?",
                "Are you seeing beneficial insects in your orchard?"
            ],
            'fertilization': [
                "When did you last test your soil?",
                "What's the age of your trees?",
                "What fertilizers have you used recently?",
                "Are you seeing any nutrient deficiency symptoms?"
            ],
            'harvesting': [
                "What variety of macadamias do you have?",
                "Are nuts starting to fall naturally?",
                "What's your typical harvest season?",
                "How do you currently assess nut maturity?"
            ],
            'certification': [
                "Are you currently farming conventionally?",
                "Which certification are you interested in?",
                "How long have you been avoiding synthetic inputs?",
                "Do you have detailed farm records?"
            ]
        }
        
        questions = followup_questions.get(domain, [
            "Can you tell me more about your farm?",
            "What specific challenges are you facing?",
            "What's your experience level with macadamia farming?"
        ])
        
        # Limit to 3 most relevant questions
        return questions[:3]

