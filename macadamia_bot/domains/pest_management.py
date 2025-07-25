"""
Pest Management Advisory Module
===============================

Provides comprehensive pest management advice for macadamia farming
using organic and integrated pest management approaches.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PestManagementAdvisor:
    """
    Provides expert pest management advice for macadamia farming
    """
    
    def __init__(self):
        """Initialize the pest management advisor"""
        self.pest_knowledge = self._load_pest_knowledge()
    
    def _load_pest_knowledge(self) -> Dict[str, Any]:
        """Load pest management knowledge base"""
        try:
            with open('macadamia_bot/data/pest_management.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Could not load pest knowledge: {e}")
            return {}
    
    def get_advice(self, 
                   query: str, 
                   parameters: Dict[str, Any] = None,
                   farm_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get pest management advice based on query and parameters
        
        Args:
            query: User's pest management question
            parameters: Extracted parameters from query
            farm_data: Farm-specific data
            
        Returns:
            Comprehensive pest management advice
        """
        try:
            # Identify specific pest if mentioned
            specific_pest = self._identify_pest_from_query(query)
            
            # Get general IPM advice
            ipm_advice = self._get_ipm_advice()
            
            # Get specific pest advice if identified
            pest_specific_advice = None
            if specific_pest:
                pest_specific_advice = self._get_specific_pest_advice(specific_pest)
            
            # Get seasonal advice
            seasonal_advice = self._get_seasonal_advice(farm_data)
            
            # Get monitoring recommendations
            monitoring_advice = self._get_monitoring_advice(farm_data)
            
            # Combine advice
            final_advice = self._combine_pest_advice(
                ipm_advice, pest_specific_advice, seasonal_advice, monitoring_advice
            )
            
            return {
                'advice': final_advice,
                'specific_pest': specific_pest,
                'ipm_principles': ipm_advice,
                'monitoring_schedule': monitoring_advice,
                'organic_treatments': self._get_organic_treatments(),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating pest management advice: {e}")
            return self._fallback_advice()
    
    def _identify_pest_from_query(self, query: str) -> Optional[str]:
        """Identify specific pest mentioned in query"""
        pest_keywords = {
            'macadamia_nut_borer': ['borer', 'nut borer', 'cryptophlebia'],
            'stink_bugs': ['stink bug', 'shield bug', 'nezara'],
            'scale_insects': ['scale', 'scale insect', 'honeydew']
        }
        
        query_lower = query.lower()
        for pest, keywords in pest_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return pest
        
        return None
    
    def _get_ipm_advice(self) -> Dict[str, Any]:
        """Get integrated pest management advice"""
        return {
            'principles': [
                'Prevention is better than treatment',
                'Regular monitoring and early detection',
                'Use of beneficial insects and natural enemies',
                'Targeted treatments only when necessary',
                'Rotation of treatment methods to prevent resistance'
            ],
            'monitoring_frequency': 'Weekly visual inspections during growing season',
            'treatment_threshold': 'Treat only when pest levels exceed economic thresholds'
        }
    
    def _get_specific_pest_advice(self, pest_name: str) -> Dict[str, Any]:
        """Get advice for specific pest"""
        if not self.pest_knowledge:
            return {}
        
        pest_data = self.pest_knowledge.get('common_pests', {}).get(pest_name, {})
        
        return {
            'description': pest_data.get('description', ''),
            'symptoms': pest_data.get('symptoms', []),
            'organic_treatments': pest_data.get('organic_treatments', []),
            'prevention': pest_data.get('prevention', []),
            'timing': pest_data.get('timing', '')
        }
    
    def _get_seasonal_advice(self, farm_data: Dict[str, Any] = None) -> str:
        """Get seasonal pest management advice"""
        if not farm_data or 'season' not in farm_data:
            return "Monitor pest activity according to seasonal patterns"
        
        season = farm_data['season'].lower()
        seasonal_advice = {
            'spring': "Increase monitoring as pest activity increases with warming weather",
            'summer': "Peak pest season - intensive monitoring and treatment may be needed",
            'autumn': "Monitor harvest areas and maintain sanitation",
            'winter': "Reduced pest activity - focus on orchard cleanup and planning"
        }
        
        return seasonal_advice.get(season, "Monitor according to local seasonal patterns")
    
    def _get_monitoring_advice(self, farm_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get monitoring recommendations"""
        return {
            'frequency': 'Weekly during growing season, bi-weekly during dormant season',
            'what_to_check': [
                'Leaves for damage or discoloration',
                'Nuts for holes or premature drop',
                'Branches for scale insects or honeydew',
                'Beneficial insect populations',
                'Pheromone trap catches'
            ],
            'record_keeping': [
                'Date and location of inspection',
                'Pest species and population levels',
                'Damage assessment',
                'Weather conditions',
                'Treatment decisions and results'
            ]
        }
    
    def _get_organic_treatments(self) -> Dict[str, List[str]]:
        """Get organic treatment options"""
        return {
            'biological_control': [
                'Beneficial insects (ladybugs, lacewings)',
                'Parasitic wasps',
                'Bacillus thuringiensis (Bt)',
                'Beneficial nematodes'
            ],
            'botanical_pesticides': [
                'Neem oil',
                'Pyrethrin sprays',
                'Insecticidal soap',
                'Horticultural oils'
            ],
            'physical_methods': [
                'Pheromone traps',
                'Sticky traps',
                'Tree bands',
                'Hand picking (small infestations)'
            ],
            'cultural_practices': [
                'Orchard sanitation',
                'Pruning for air circulation',
                'Weed management',
                'Habitat for beneficial insects'
            ]
        }
    
    def _combine_pest_advice(self, ipm_advice, pest_specific, seasonal, monitoring):
        """Combine all pest advice components"""
        advice_parts = []
        
        advice_parts.append("🛡️ **Integrated Pest Management Approach:**")
        for principle in ipm_advice['principles'][:3]:
            advice_parts.append(f"• {principle}")
        
        if pest_specific:
            advice_parts.append(f"\n🐛 **Specific Pest Management:**")
            if pest_specific.get('organic_treatments'):
                advice_parts.append("Recommended treatments:")
                for treatment in pest_specific['organic_treatments'][:3]:
                    advice_parts.append(f"• {treatment}")
        
        advice_parts.append(f"\n📅 **Seasonal Considerations:**")
        advice_parts.append(f"• {seasonal}")
        
        advice_parts.append(f"\n🔍 **Monitoring Schedule:**")
        advice_parts.append(f"• {monitoring['frequency']}")
        advice_parts.append("• Focus on leaves, nuts, and beneficial insects")
        
        return "\n".join(advice_parts)
    
    def _fallback_advice(self) -> Dict[str, Any]:
        """Fallback advice when processing fails"""
        return {
            'advice': """🛡️ **Organic Pest Management for Macadamias:**

• **Prevention First:** Maintain healthy trees through proper nutrition and care
• **Regular Monitoring:** Weekly inspections during growing season
• **Beneficial Insects:** Encourage natural predators with diverse plantings
• **Organic Treatments:** Use neem oil, insecticidal soap, or Bt when needed
• **Sanitation:** Remove fallen nuts and debris promptly

Focus on building a balanced ecosystem that naturally controls pests.""",
            'organic_treatments': self._get_organic_treatments(),
            'timestamp': datetime.now().isoformat(),
            'note': 'Fallback advice provided'
        }

