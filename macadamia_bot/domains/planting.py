"""
Planting Advisory Module
========================

Provides comprehensive planting advice for macadamia farming including
site selection, timing, varieties, and establishment practices.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class PlantingAdvisor:
    """
    Provides expert planting advice for macadamia farming
    """
    
    def __init__(self):
        """Initialize the planting advisor"""
        self.planting_knowledge = self._load_planting_knowledge()
    
    def _load_planting_knowledge(self) -> Dict[str, Any]:
        """Load planting knowledge base"""
        try:
            with open('macadamia_bot/data/planting_calendar.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Could not load planting knowledge: {e}")
            return {}
    
    def get_advice(self, 
                   query: str, 
                   parameters: Dict[str, Any] = None,
                   farm_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get planting advice based on query and parameters
        
        Args:
            query: User's planting question
            parameters: Extracted parameters from query
            farm_data: Farm-specific data
            
        Returns:
            Comprehensive planting advice
        """
        try:
            advice_components = {}
            
            # Determine what type of planting advice is needed
            if self._is_site_selection_query(query):
                advice_components['site_selection'] = self._get_site_selection_advice(farm_data)
            
            if self._is_timing_query(query):
                advice_components['timing'] = self._get_planting_timing_advice(parameters, farm_data)
            
            if self._is_variety_query(query):
                advice_components['varieties'] = self._get_variety_advice(parameters, farm_data)
            
            if self._is_spacing_query(query):
                advice_components['spacing'] = self._get_spacing_advice(parameters, farm_data)
            
            if self._is_establishment_query(query):
                advice_components['establishment'] = self._get_establishment_advice(parameters)
            
            # If no specific category, provide general planting advice
            if not advice_components:
                advice_components['general'] = self._get_general_planting_advice()
            
            # Combine advice components
            final_advice = self._combine_advice_components(advice_components)
            
            return {
                'advice': final_advice,
                'components': advice_components,
                'recommendations': self._get_specific_recommendations(advice_components),
                'next_steps': self._get_next_steps(advice_components),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating planting advice: {e}")
            return self._fallback_advice()
    
    def _is_site_selection_query(self, query: str) -> bool:
        """Check if query is about site selection"""
        site_keywords = ['site', 'location', 'where', 'soil', 'drainage', 'slope', 'climate']
        return any(keyword in query.lower() for keyword in site_keywords)
    
    def _is_timing_query(self, query: str) -> bool:
        """Check if query is about planting timing"""
        timing_keywords = ['when', 'time', 'season', 'month', 'timing', 'best time']
        return any(keyword in query.lower() for keyword in timing_keywords)
    
    def _is_variety_query(self, query: str) -> bool:
        """Check if query is about variety selection"""
        variety_keywords = ['variety', 'cultivar', 'type', 'which', 'best variety', 'recommend']
        return any(keyword in query.lower() for keyword in variety_keywords)
    
    def _is_spacing_query(self, query: str) -> bool:
        """Check if query is about tree spacing"""
        spacing_keywords = ['spacing', 'distance', 'apart', 'density', 'layout']
        return any(keyword in query.lower() for keyword in spacing_keywords)
    
    def _is_establishment_query(self, query: str) -> bool:
        """Check if query is about tree establishment"""
        establishment_keywords = ['establish', 'care', 'after planting', 'young trees', 'maintenance']
        return any(keyword in query.lower() for keyword in establishment_keywords)
    
    def _get_site_selection_advice(self, farm_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get site selection advice"""
        
        site_advice = {
            'soil_requirements': {
                'type': 'Well-draining, deep volcanic or alluvial soils',
                'ph': '6.0-6.5 optimal range',
                'depth': 'Minimum 1.5m deep soil',
                'drainage': 'Good drainage essential - avoid waterlogged areas'
            },
            'climate_needs': {
                'temperature': '18-25°C optimal growing range',
                'rainfall': '1000-2000mm annually, well distributed',
                'humidity': '60-80% relative humidity',
                'frost': 'Protection needed for young trees'
            },
            'topography': {
                'slope': 'Gentle slopes preferred (2-15%)',
                'aspect': 'North-facing slopes in Southern Hemisphere',
                'elevation': 'Sea level to 800m elevation suitable',
                'wind_protection': 'Shelter from strong winds essential'
            }
        }
        
        # Add specific recommendations based on farm data
        if farm_data:
            recommendations = []
            
            if 'soil_ph' in farm_data:
                ph = farm_data['soil_ph']
                if ph < 6.0:
                    recommendations.append(f"Your soil pH ({ph}) is slightly low. Consider lime application to raise pH to 6.0-6.5")
                elif ph > 6.5:
                    recommendations.append(f"Your soil pH ({ph}) is slightly high. Add organic matter to help buffer pH")
                else:
                    recommendations.append(f"Your soil pH ({ph}) is in the optimal range for macadamias")
            
            if 'farm_location' in farm_data:
                recommendations.append(f"Consider local climate patterns for {farm_data['farm_location']}")
            
            site_advice['specific_recommendations'] = recommendations
        
        return site_advice
    
    def _get_planting_timing_advice(self, 
                                  parameters: Dict[str, Any] = None,
                                  farm_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get planting timing advice"""
        
        timing_advice = {
            'optimal_seasons': {
                'spring': {
                    'months': 'September-November (Southern Hemisphere)',
                    'advantages': [
                        'Full growing season ahead',
                        'Optimal soil temperatures',
                        'Reduced transplant shock'
                    ],
                    'considerations': [
                        'Ensure adequate water supply',
                        'Monitor for spring pests',
                        'Protect from late frosts'
                    ]
                },
                'autumn': {
                    'months': 'March-May (Southern Hemisphere)',
                    'advantages': [
                        'Mild temperatures reduce stress',
                        'Winter rains help establishment',
                        'Less irrigation required'
                    ],
                    'considerations': [
                        'Plant early enough before winter',
                        'Protect from winter winds',
                        'Ensure good drainage'
                    ]
                }
            },
            'avoid_periods': [
                'Peak summer heat (December-February)',
                'Frost periods (June-August in cold areas)',
                'Waterlogged conditions after heavy rains'
            ]
        }
        
        # Add current season recommendation
        current_month = datetime.now().month
        if farm_data and 'season' in farm_data:
            current_season = farm_data['season']
            timing_advice['current_recommendation'] = self._get_current_season_advice(current_season)
        
        return timing_advice
    
    def _get_variety_advice(self, 
                          parameters: Dict[str, Any] = None,
                          farm_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get variety selection advice"""
        
        if not self.planting_knowledge:
            return {'error': 'Variety information not available'}
        
        variety_info = self.planting_knowledge.get('planting_guide', {}).get('variety_selection', {})
        
        variety_advice = {
            'popular_varieties': variety_info.get('popular_varieties', {}),
            'selection_criteria': variety_info.get('selection_criteria', []),
            'recommendations': []
        }
        
        # Add specific recommendations based on parameters
        if parameters:
            if 'variety' in parameters:
                specific_variety = parameters['variety']
                if specific_variety in variety_advice['popular_varieties']:
                    variety_data = variety_advice['popular_varieties'][specific_variety]
                    variety_advice['specific_variety_info'] = {
                        'name': specific_variety,
                        'details': variety_data
                    }
        
        # Add climate-based recommendations
        if farm_data:
            climate_recommendations = []
            
            if 'temperature' in farm_data:
                temp = farm_data['temperature']
                if temp > 26:
                    climate_recommendations.append("Consider heat-tolerant varieties like A38")
                elif temp < 20:
                    climate_recommendations.append("Consider cold-hardy varieties like Beaumont")
            
            if climate_recommendations:
                variety_advice['climate_recommendations'] = climate_recommendations
        
        return variety_advice
    
    def _get_spacing_advice(self, 
                          parameters: Dict[str, Any] = None,
                          farm_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get tree spacing advice"""
        
        spacing_info = self.planting_knowledge.get('planting_guide', {}).get('tree_spacing', {})
        
        spacing_advice = {
            'spacing_options': spacing_info,
            'recommendation': 'Traditional 8m x 8m spacing recommended for most situations'
        }
        
        # Add specific recommendations based on farm size and management
        if farm_data:
            recommendations = []
            
            if 'orchard_size' in farm_data:
                size = farm_data['orchard_size']
                if isinstance(size, (int, float)) and size < 2:
                    recommendations.append("For small orchards, consider intensive 6m x 6m spacing")
                elif isinstance(size, (int, float)) and size > 10:
                    recommendations.append("For large orchards, traditional 8m x 8m spacing allows mechanization")
            
            if 'farming_experience' in farm_data:
                experience = farm_data['farming_experience']
                if isinstance(experience, (int, float)) and experience < 3:
                    recommendations.append("New farmers should start with traditional spacing for easier management")
            
            if recommendations:
                spacing_advice['specific_recommendations'] = recommendations
        
        return spacing_advice
    
    def _get_establishment_advice(self, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get tree establishment advice"""
        
        establishment_info = self.planting_knowledge.get('planting_guide', {}).get('planting_procedure', {})
        
        establishment_advice = {
            'planting_steps': establishment_info.get('planting_steps', []),
            'post_planting_care': establishment_info.get('post_planting_care', {}),
            'first_year_care': [
                'Water deeply 2-3 times per week',
                'Maintain 10cm mulch layer around trees',
                'Monitor for pests and diseases',
                'Protect from strong winds',
                'Avoid fertilizing for first 6 weeks'
            ],
            'establishment_timeline': self.planting_knowledge.get('establishment_timeline', {})
        }
        
        return establishment_advice
    
    def _get_general_planting_advice(self) -> Dict[str, Any]:
        """Get general planting advice"""
        
        return {
            'key_principles': [
                'Choose the right site with good drainage and climate',
                'Select appropriate varieties for your conditions',
                'Plant at optimal times (spring or autumn)',
                'Use proper spacing for long-term growth',
                'Provide excellent establishment care'
            ],
            'success_factors': [
                'Site preparation is crucial for long-term success',
                'Quality nursery trees from reputable suppliers',
                'Consistent watering during establishment',
                'Protection from pests and environmental stress',
                'Patience - trees take 4-7 years to reach production'
            ]
        }
    
    def _get_current_season_advice(self, season: str) -> str:
        """Get advice for current season"""
        
        season_advice = {
            'spring': "Excellent time for planting! Soil is warming up and growing season is ahead. Ensure adequate water supply and monitor for pests.",
            'summer': "Not ideal for planting due to heat stress. If you must plant, provide extra shade and water frequently. Consider waiting for autumn.",
            'autumn': "Good planting time with mild temperatures and upcoming winter rains. Plant early in autumn to allow establishment before winter.",
            'winter': "Generally not recommended for planting due to cold stress and slow growth. Prepare sites and plan for spring planting."
        }
        
        return season_advice.get(season.lower(), "Consider local climate conditions for optimal planting timing.")
    
    def _combine_advice_components(self, components: Dict[str, Any]) -> str:
        """Combine advice components into coherent response"""
        
        advice_parts = []
        
        if 'site_selection' in components:
            advice_parts.append("🏞️ **Site Selection:**")
            site_info = components['site_selection']
            if 'specific_recommendations' in site_info:
                for rec in site_info['specific_recommendations']:
                    advice_parts.append(f"• {rec}")
            else:
                advice_parts.append("• Choose well-draining soil with pH 6.0-6.5")
                advice_parts.append("• Ensure protection from strong winds")
                advice_parts.append("• Select sites with good air circulation")
        
        if 'timing' in components:
            advice_parts.append("\n📅 **Planting Timing:**")
            if 'current_recommendation' in components['timing']:
                advice_parts.append(f"• {components['timing']['current_recommendation']}")
            advice_parts.append("• Spring (Sep-Nov) and Autumn (Mar-May) are optimal")
            advice_parts.append("• Avoid extreme weather periods")
        
        if 'varieties' in components:
            advice_parts.append("\n🌱 **Variety Selection:**")
            varieties = components['varieties'].get('popular_varieties', {})
            if varieties:
                for variety, info in list(varieties.items())[:3]:  # Show top 3
                    advice_parts.append(f"• {variety.title()}: {info.get('characteristics', 'Good choice')}")
        
        if 'spacing' in components:
            advice_parts.append("\n📏 **Tree Spacing:**")
            advice_parts.append("• Traditional: 8m x 8m (156 trees/hectare)")
            advice_parts.append("• Intensive: 6m x 6m (278 trees/hectare)")
            if 'specific_recommendations' in components['spacing']:
                for rec in components['spacing']['specific_recommendations']:
                    advice_parts.append(f"• {rec}")
        
        if 'establishment' in components:
            advice_parts.append("\n🌿 **Establishment Care:**")
            advice_parts.append("• Water deeply 2-3 times per week")
            advice_parts.append("• Maintain mulch layer around trees")
            advice_parts.append("• Monitor and protect from pests")
            advice_parts.append("• Be patient - production starts in 4-7 years")
        
        if 'general' in components:
            advice_parts.append("🌳 **General Planting Principles:**")
            for principle in components['general']['key_principles']:
                advice_parts.append(f"• {principle}")
        
        return "\n".join(advice_parts) if advice_parts else "I'd be happy to help with your planting questions!"
    
    def _get_specific_recommendations(self, components: Dict[str, Any]) -> List[str]:
        """Get specific actionable recommendations"""
        
        recommendations = []
        
        # Extract specific recommendations from each component
        for component_name, component_data in components.items():
            if isinstance(component_data, dict):
                if 'specific_recommendations' in component_data:
                    recommendations.extend(component_data['specific_recommendations'])
                elif 'recommendations' in component_data:
                    recommendations.extend(component_data['recommendations'])
        
        # Add general recommendations if none found
        if not recommendations:
            recommendations = [
                "Test soil pH and drainage before planting",
                "Choose varieties suited to your climate",
                "Plan for long-term tree spacing needs",
                "Prepare planting sites well in advance",
                "Source quality trees from reputable nurseries"
            ]
        
        return recommendations[:5]  # Limit to top 5
    
    def _get_next_steps(self, components: Dict[str, Any]) -> List[str]:
        """Get suggested next steps"""
        
        next_steps = []
        
        if 'site_selection' in components:
            next_steps.append("Conduct soil test for pH and nutrient levels")
            next_steps.append("Assess drainage and prepare planting sites")
        
        if 'timing' in components:
            next_steps.append("Plan planting schedule based on optimal timing")
        
        if 'varieties' in components:
            next_steps.append("Research and select appropriate varieties")
            next_steps.append("Source quality nursery trees")
        
        if 'spacing' in components:
            next_steps.append("Design orchard layout with proper spacing")
        
        if 'establishment' in components:
            next_steps.append("Prepare establishment care plan")
            next_steps.append("Set up irrigation system")
        
        # Default next steps if none specific
        if not next_steps:
            next_steps = [
                "Assess your site conditions",
                "Research suitable varieties",
                "Plan your planting timeline",
                "Prepare necessary resources"
            ]
        
        return next_steps[:4]  # Limit to top 4
    
    def _fallback_advice(self) -> Dict[str, Any]:
        """Fallback advice when processing fails"""
        
        return {
            'advice': """For successful macadamia planting:
            
🏞️ **Site Selection:** Choose well-draining soil with pH 6.0-6.5, protection from winds, and good air circulation.

📅 **Timing:** Plant in spring (Sep-Nov) or autumn (Mar-May) for best establishment.

🌱 **Varieties:** Popular choices include Beaumont, A4, A16, and A38. Choose based on your climate and market needs.

📏 **Spacing:** Traditional 8m x 8m spacing works well for most situations.

🌿 **Care:** Water regularly, mulch well, and be patient - production starts in 4-7 years.""",
            'recommendations': [
                "Test soil conditions before planting",
                "Choose appropriate varieties for your climate",
                "Plan for proper tree spacing",
                "Prepare establishment care plan"
            ],
            'next_steps': [
                "Assess your planting site",
                "Research variety options",
                "Plan your timeline",
                "Source quality nursery trees"
            ],
            'timestamp': datetime.now().isoformat(),
            'note': 'Fallback advice provided'
        }

