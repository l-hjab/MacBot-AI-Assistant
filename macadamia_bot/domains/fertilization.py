"""
Fertilization Advisory Module
=============================

Provides comprehensive organic fertilization advice for macadamia farming.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FertilizationAdvisor:
    """
    Provides expert fertilization advice for macadamia farming
    """
    
    def __init__(self):
        """Initialize the fertilization advisor"""
        self.fertilization_knowledge = self._load_fertilization_knowledge()
    
    def _load_fertilization_knowledge(self) -> Dict[str, Any]:
        """Load fertilization knowledge base"""
        try:
            with open('macadamia_bot/data/fertilization_guide.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Could not load fertilization knowledge: {e}")
            return {}
    
    def get_advice(self, 
                   query: str, 
                   parameters: Dict[str, Any] = None,
                   farm_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get fertilization advice"""
        try:
            # Determine tree age category
            tree_age_category = self._determine_tree_age_category(parameters, farm_data)
            
            # Get seasonal fertilization schedule
            seasonal_schedule = self._get_seasonal_schedule(tree_age_category, farm_data)
            
            # Get soil-specific recommendations
            soil_recommendations = self._get_soil_recommendations(farm_data)
            
            # Get organic fertilizer options
            organic_options = self._get_organic_fertilizer_options()
            
            # Combine advice
            final_advice = self._combine_fertilization_advice(
                seasonal_schedule, soil_recommendations, organic_options, tree_age_category
            )
            
            return {
                'advice': final_advice,
                'tree_age_category': tree_age_category,
                'seasonal_schedule': seasonal_schedule,
                'soil_recommendations': soil_recommendations,
                'organic_options': organic_options,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating fertilization advice: {e}")
            return self._fallback_advice()
    
    def _determine_tree_age_category(self, parameters, farm_data):
        """Determine tree age category"""
        tree_age = None
        
        if parameters and 'tree_age' in parameters:
            tree_age = parameters['tree_age']
        elif farm_data and 'tree_age' in farm_data:
            tree_age = farm_data['tree_age']
        
        if tree_age is None:
            return 'unknown'
        elif tree_age <= 3:
            return 'young'
        else:
            return 'mature'
    
    def _get_seasonal_schedule(self, tree_age_category, farm_data):
        """Get seasonal fertilization schedule"""
        if not self.fertilization_knowledge:
            return {}
        
        fertilization_data = self.fertilization_knowledge.get('organic_fertilization', {})
        schedule_data = fertilization_data.get('fertilization_schedule', {})
        
        if tree_age_category == 'young':
            return schedule_data.get('young_trees_1_3_years', {})
        elif tree_age_category == 'mature':
            return schedule_data.get('mature_trees_4_plus_years', {})
        else:
            return {}
    
    def _get_soil_recommendations(self, farm_data):
        """Get soil-specific recommendations"""
        recommendations = []
        
        if farm_data and 'soil_ph' in farm_data:
            ph = farm_data['soil_ph']
            if ph < 6.0:
                recommendations.append(f"Soil pH ({ph}) is low - add lime to raise to 6.0-6.5")
            elif ph > 6.5:
                recommendations.append(f"Soil pH ({ph}) is high - add sulfur or organic matter")
            else:
                recommendations.append(f"Soil pH ({ph}) is optimal for macadamias")
        
        return recommendations
    
    def _get_organic_fertilizer_options(self):
        """Get organic fertilizer options"""
        return {
            'nitrogen_sources': ['Blood meal', 'Fish emulsion', 'Compost'],
            'phosphorus_sources': ['Bone meal', 'Rock phosphate'],
            'potassium_sources': ['Kelp meal', 'Wood ash', 'Compost'],
            'complete_fertilizers': ['Aged manure', 'Compost', 'Organic blends']
        }
    
    def _combine_fertilization_advice(self, seasonal_schedule, soil_recs, organic_options, tree_age):
        """Combine fertilization advice components"""
        advice_parts = []
        
        advice_parts.append("🌱 **Organic Fertilization Program:**")
        
        if tree_age == 'young':
            advice_parts.append("For young trees (1-3 years):")
            advice_parts.append("• Spring: 10-15kg compost + 0.5kg blood meal per tree")
            advice_parts.append("• Summer: Monthly fish emulsion (1:10 dilution)")
            advice_parts.append("• Autumn: 5-10kg aged manure per tree")
        elif tree_age == 'mature':
            advice_parts.append("For mature trees (4+ years):")
            advice_parts.append("• Spring: 20-30kg compost + 1-2kg blood meal per tree")
            advice_parts.append("• Summer: Monthly fish emulsion + foliar seaweed spray")
            advice_parts.append("• Autumn: 15-25kg aged manure + rock phosphate")
        else:
            advice_parts.append("• Apply compost in spring and autumn")
            advice_parts.append("• Use organic fertilizers based on soil test results")
            advice_parts.append("• Maintain soil pH between 6.0-6.5")
        
        if soil_recs:
            advice_parts.append("\n🧪 **Soil-Specific Recommendations:**")
            for rec in soil_recs:
                advice_parts.append(f"• {rec}")
        
        advice_parts.append("\n📋 **Key Organic Fertilizers:**")
        advice_parts.append("• Compost: Improves soil structure and provides balanced nutrition")
        advice_parts.append("• Blood meal: Quick nitrogen source for growth")
        advice_parts.append("• Kelp meal: Trace elements and growth hormones")
        advice_parts.append("• Fish emulsion: Liquid fertilizer for regular feeding")
        
        return "\n".join(advice_parts)
    
    def _fallback_advice(self):
        """Fallback fertilization advice"""
        return {
            'advice': """🌱 **Organic Fertilization for Macadamias:**

• **Soil Testing:** Test annually to determine specific nutrient needs
• **Compost:** Apply 10-30kg per tree in spring and autumn
• **Organic Fertilizers:** Use blood meal, bone meal, and kelp meal
• **pH Management:** Maintain soil pH between 6.0-6.5
• **Foliar Feeding:** Monthly fish emulsion during growing season

Adjust amounts based on tree age and soil test results.""",
            'timestamp': datetime.now().isoformat(),
            'note': 'Fallback advice provided'
        }

