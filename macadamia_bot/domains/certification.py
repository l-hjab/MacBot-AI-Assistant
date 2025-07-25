"""
Certification Advisory Module
=============================

Provides comprehensive organic certification advice for macadamia farming.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CertificationAdvisor:
    """
    Provides expert certification advice for macadamia farming
    """
    
    def __init__(self):
        """Initialize the certification advisor"""
        self.certification_knowledge = self._load_certification_knowledge()
    
    def _load_certification_knowledge(self) -> Dict[str, Any]:
        """Load certification knowledge base"""
        try:
            with open('macadamia_bot/data/certification_guide.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Could not load certification knowledge: {e}")
            return {}
    
    def get_advice(self, 
                   query: str, 
                   parameters: Dict[str, Any] = None,
                   farm_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get certification advice"""
        try:
            # Get certification requirements
            requirements = self._get_certification_requirements()
            
            # Get process steps
            process_steps = self._get_certification_process()
            
            # Get record keeping advice
            record_keeping = self._get_record_keeping_advice()
            
            # Get transition advice
            transition_advice = self._get_transition_advice()
            
            # Combine advice
            final_advice = self._combine_certification_advice(
                requirements, process_steps, record_keeping, transition_advice
            )
            
            return {
                'advice': final_advice,
                'requirements': requirements,
                'process_steps': process_steps,
                'record_keeping': record_keeping,
                'transition_advice': transition_advice,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating certification advice: {e}")
            return self._fallback_advice()
    
    def _get_certification_requirements(self):
        """Get certification requirements"""
        if not self.certification_knowledge:
            return {}
        
        return self.certification_knowledge.get('organic_certification', {}).get('certification_requirements', {})
    
    def _get_certification_process(self):
        """Get certification process steps"""
        if not self.certification_knowledge:
            return {}
        
        return self.certification_knowledge.get('certification_process', {})
    
    def _get_record_keeping_advice(self):
        """Get record keeping requirements"""
        if not self.certification_knowledge:
            return {}
        
        return self.certification_knowledge.get('organic_certification', {}).get('record_keeping_requirements', {})
    
    def _get_transition_advice(self):
        """Get transition period advice"""
        return {
            'duration': '3 years minimum from last prohibited substance use',
            'key_activities': [
                'Stop using all prohibited substances immediately',
                'Begin detailed record keeping',
                'Implement organic practices',
                'Plan for annual inspections'
            ]
        }
    
    def _combine_certification_advice(self, requirements, process, records, transition):
        """Combine certification advice components"""
        advice_parts = []
        
        advice_parts.append("🏆 **Organic Certification Process:**")
        advice_parts.append("• 3-year transition period required")
        advice_parts.append("• Stop all prohibited substances immediately")
        advice_parts.append("• Begin detailed record keeping now")
        advice_parts.append("• Choose accredited certification body")
        advice_parts.append("• Undergo annual inspections")
        
        advice_parts.append("\n📋 **Key Requirements:**")
        advice_parts.append("• No synthetic fertilizers or pesticides")
        advice_parts.append("• Use only approved organic inputs")
        advice_parts.append("• Maintain buffer zones from conventional farms")
        advice_parts.append("• Keep detailed production records")
        
        advice_parts.append("\n📝 **Record Keeping Essentials:**")
        advice_parts.append("• All input purchases and applications")
        advice_parts.append("• Field maps and crop rotation plans")
        advice_parts.append("• Harvest dates and quantities")
        advice_parts.append("• Storage and handling procedures")
        
        advice_parts.append("\n⏰ **Timeline:**")
        advice_parts.append("• Start transition immediately")
        advice_parts.append("• Apply for certification in year 2")
        advice_parts.append("• Full certification after 3 years")
        advice_parts.append("• Annual renewals required")
        
        return "\n".join(advice_parts)
    
    def _fallback_advice(self):
        """Fallback certification advice"""
        return {
            'advice': """🏆 **Organic Certification for Macadamias:**

• **Transition Period:** 3 years minimum without prohibited substances
• **Record Keeping:** Document everything - inputs, practices, harvests
• **Approved Inputs:** Use only OMRI-listed or certifier-approved materials
• **Inspection:** Annual on-farm inspections required
• **Certification Body:** Choose accredited certifier for your region

Start record keeping immediately, even before formal certification begins.""",
            'timestamp': datetime.now().isoformat(),
            'note': 'Fallback advice provided'
        }

