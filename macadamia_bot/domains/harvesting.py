"""
Harvesting Advisory Module
==========================

Provides comprehensive harvesting advice for macadamia farming.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HarvestingAdvisor:
    """
    Provides expert harvesting advice for macadamia farming
    """
    
    def __init__(self):
        """Initialize the harvesting advisor"""
        self.harvest_knowledge = self._load_harvest_knowledge()
    
    def _load_harvest_knowledge(self) -> Dict[str, Any]:
        """Load harvest knowledge base"""
        try:
            with open('macadamia_bot/data/harvest_timing.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Could not load harvest knowledge: {e}")
            return {}
    
    def get_advice(self, 
                   query: str, 
                   parameters: Dict[str, Any] = None,
                   farm_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get harvesting advice"""
        try:
            # Get maturity indicators
            maturity_advice = self._get_maturity_indicators()
            
            # Get harvest methods
            harvest_methods = self._get_harvest_methods()
            
            # Get post-harvest handling
            post_harvest = self._get_post_harvest_advice()
            
            # Get seasonal timing
            seasonal_timing = self._get_seasonal_timing(farm_data)
            
            # Combine advice
            final_advice = self._combine_harvest_advice(
                maturity_advice, harvest_methods, post_harvest, seasonal_timing
            )
            
            return {
                'advice': final_advice,
                'maturity_indicators': maturity_advice,
                'harvest_methods': harvest_methods,
                'post_harvest_handling': post_harvest,
                'seasonal_timing': seasonal_timing,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating harvest advice: {e}")
            return self._fallback_advice()
    
    def _get_maturity_indicators(self):
        """Get maturity indicators"""
        if not self.harvest_knowledge:
            return {}
        
        return self.harvest_knowledge.get('harvest_guide', {}).get('maturity_indicators', {})
    
    def _get_harvest_methods(self):
        """Get harvest methods"""
        if not self.harvest_knowledge:
            return {}
        
        return self.harvest_knowledge.get('harvest_guide', {}).get('harvest_methods', {})
    
    def _get_post_harvest_advice(self):
        """Get post-harvest handling advice"""
        if not self.harvest_knowledge:
            return {}
        
        return self.harvest_knowledge.get('harvest_guide', {}).get('post_harvest_handling', {})
    
    def _get_seasonal_timing(self, farm_data):
        """Get seasonal timing advice"""
        if not farm_data or 'season' not in farm_data:
            return "Monitor nuts for natural drop and maturity signs"
        
        season = farm_data['season'].lower()
        timing_advice = {
            'autumn': "Prime harvest season - monitor daily for nut drop",
            'winter': "Late harvest period - focus on quality assessment",
            'spring': "Post-harvest - focus on storage and processing",
            'summer': "Pre-harvest - monitor nut development"
        }
        
        return timing_advice.get(season, "Monitor according to local harvest patterns")
    
    def _combine_harvest_advice(self, maturity, methods, post_harvest, timing):
        """Combine harvest advice components"""
        advice_parts = []
        
        advice_parts.append("🥜 **Harvest Timing & Maturity:**")
        advice_parts.append("• Wait for nuts to fall naturally from trees")
        advice_parts.append("• Husk should split open and nut falls freely")
        advice_parts.append("• Perform float test: mature nuts sink in water")
        advice_parts.append("• Collect nuts within 2-3 days of falling")
        
        advice_parts.append("\n📦 **Harvest Methods:**")
        advice_parts.append("• Ground collection: Most common method")
        advice_parts.append("• Tree shaking: For controlled timing")
        advice_parts.append("• Hand picking: Highest quality but labor intensive")
        
        advice_parts.append("\n🔄 **Post-Harvest Handling:**")
        advice_parts.append("• Remove husks within 24 hours")
        advice_parts.append("• Wash nuts to remove debris")
        advice_parts.append("• Dry to 1.5-3.5% moisture content")
        advice_parts.append("• Store in cool, dry, ventilated conditions")
        
        advice_parts.append(f"\n📅 **Current Season:**")
        advice_parts.append(f"• {timing}")
        
        return "\n".join(advice_parts)
    
    def _fallback_advice(self):
        """Fallback harvest advice"""
        return {
            'advice': """🥜 **Macadamia Harvesting Guide:**

• **Timing:** Wait for natural nut drop when husks split open
• **Collection:** Gather nuts within 2-3 days to maintain quality
• **Testing:** Use float test - mature nuts sink in water
• **Processing:** Remove husks promptly and dry to proper moisture
• **Storage:** Keep in cool, dry conditions with good ventilation

Quality handling from tree to storage is crucial for premium nuts.""",
            'timestamp': datetime.now().isoformat(),
            'note': 'Fallback advice provided'
        }

