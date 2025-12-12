import re
import requests
import json
from typing import Optional, Tuple, Dict, Any
from django.conf import settings
import google.generativeai as genai
from PIL import Image
import io

# Configure Gemini Pro
try:
    genai.configure(api_key=getattr(settings, 'GOOGLE_GEMINI_API_KEY', None))
except Exception as e:
    print(f"Warning: Gemini Pro not configured: {e}")

class GeminiProAnalyzer:
    """
    Primary AI analyzer using Google Gemini Pro Vision API.
    Provides comprehensive complaint analysis with image understanding.
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'GOOGLE_GEMINI_API_KEY', None)
        if self.api_key:
            try:
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.available = True
            except Exception as e:
                print(f"Warning: Gemini Pro model not available: {e}")
                self.available = False
        else:
            self.available = False
        
        # Complaint categories
        self.categories = {
            'road': 'Road & Infrastructure Issues',
            'water': 'Water & Pipe Problems', 
            'streetlight': 'Street Lighting Issues',
            'traffic': 'Traffic & Signal Problems',
            'garbage': 'Garbage & Waste Issues',
            'noise': 'Construction & Noise Problems',
            'other': 'Other Issues'
        }
    
    def analyze_complaint(self, title: str, description: str, image_path: Optional[str] = None) -> dict:
        """
        Analyze complaint using Gemini Pro Vision API.
        Falls back to rule-based analysis if API fails.
        """
        if self.available and image_path:
            try:
                return self._analyze_with_gemini(title, description, image_path)
            except Exception as e:
                print(f"Gemini Pro analysis failed: {e}")
                # Fall back to rule-based analysis
                return self._fallback_analysis(title, description)
        else:
            # Use rule-based analysis
            return self._fallback_analysis(title, description)
    
    def _analyze_with_gemini(self, title: str, description: str, image_path: str) -> dict:
        """
        Analyze complaint using Gemini Pro Vision API.
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Create comprehensive prompt
            prompt = f"""
            Analyze this image as a civic complaint submission for a city government system.
            
            Complaint Details:
            - Title: {title}
            - Description: {description}
            
            Please provide a detailed analysis in the following JSON format:
            {{
                "category": "road|water|streetlight|traffic|garbage|noise|other",
                "description": "Detailed description of what you see in the image",
                "severity": "low|medium|high",
                "priority": "low|medium|high",
                "estimated_resolution_time": "1-2 days|1 week|2-4 weeks|1+ months",
                "assigned_department": "Public Works|Water Services|Electrical Services|Traffic Management|Waste Management|Code Enforcement|General Services",
                "recommended_actions": [
                    "Action 1",
                    "Action 2", 
                    "Action 3",
                    "Action 4"
                ],
                "safety_concerns": "Any immediate safety risks or concerns",
                "confidence": "high|medium|low",
                "ai_insights": "Additional AI-generated insights about the issue"
            }}
            
            IMPORTANT: Use lowercase values for severity, priority, and confidence fields.
            
            Focus on:
            1. Identifying the exact nature of the problem
            2. Assessing safety risks and urgency
            3. Providing actionable recommendations for city officials
            4. Estimating realistic resolution timelines
            5. Suggesting appropriate departments to handle the issue
            
            Be specific and practical in your recommendations.
            """
            
            # Get Gemini's analysis
            response = self.model.generate_content([prompt, image])
            response_text = response.text
            
            # Parse JSON response
            try:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start != -1 and json_end != -1:
                    json_str = response_text[json_start:json_end]
                    analysis = json.loads(json_str)
                    
                    # Ensure category is valid
                    category = analysis.get('category', 'other')
                    if category not in ['road', 'water', 'streetlight', 'traffic', 'garbage', 'noise', 'other']:
                        category = 'other'
                    
                    return {
                        'success': True,
                        'ai_provider': 'Gemini Pro',
                        'category': category,
                        'description': analysis.get('description', 'No description available'),
                        'severity_level': analysis.get('severity', 'medium').lower(),
                        'priority_level': analysis.get('priority', 'medium').lower(),
                        'estimated_resolution_time': analysis.get('estimated_resolution_time', '1-2 weeks'),
                        'assigned_department': analysis.get('assigned_department', 'General Services'),
                        'suggested_actions': analysis.get('recommended_actions', []),
                        'safety_concerns': analysis.get('safety_concerns', 'No immediate safety concerns'),
                        'confidence': analysis.get('confidence', 'medium'),
                        'ai_insights': analysis.get('ai_insights', 'AI analysis completed'),
                        'raw_ai_response': response_text,
                        'analysis_method': 'Gemini Pro Vision API'
                    }
                else:
                    raise ValueError("No JSON found in response")
                    
            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON parsing failed: {e}")
                # Use fallback analysis
                return self._fallback_analysis(title, description)
                
        except Exception as e:
            print(f"Gemini Pro API error: {e}")
            return self._fallback_analysis(title, description)
    
    def _fallback_analysis(self, title: str, description: str) -> dict:
        """
        Fallback rule-based analysis when AI API is not available.
        """
        print(f"🔍 Running fallback analysis for: '{title}' - '{description}'")
        
        classifier = RuleBasedClassifier()
        category, confidence = classifier.classify_complaint(title, description)
        
        # Get category details
        category_info = classifier.get_category_details(category)
        
        result = {
            'success': True,
            'ai_provider': 'Rule-Based Analysis',
            'category': category,
            'description': f"Rule-based classification: {category_info['display_name']}",
            'severity_level': self._assess_severity(title, description),
            'priority_level': category_info['priority'],
            'estimated_resolution_time': category_info['resolution_time'],
            'assigned_department': category_info['department'],
            'suggested_actions': category_info['actions'],
            'safety_concerns': 'Standard safety protocols apply',
            'confidence': confidence,
            'ai_insights': f"Classified using keyword matching with {confidence:.1%} confidence",
            'raw_ai_response': 'Rule-based analysis used',
            'analysis_method': 'Rule-Based Classification'
        }
        
        print(f"📊 Fallback analysis result: Category={result['category']}, Severity={result['severity_level']}, Priority={result['priority_level']}")
        return result
    
    def _assess_severity(self, title: str, description: str) -> str:
        """Assess severity based on keywords"""
        text = f"{title} {description}".lower()
        
        high_severity = ['emergency', 'dangerous', 'urgent', 'critical', 'broken', 'damage', 'accident', 'injury', 'fire', 'flood']
        medium_severity = ['problem', 'issue', 'concern', 'annoying', 'inconvenient', 'blocked', 'overflow']
        
        severity = 'low'
        if any(word in text for word in high_severity):
            severity = 'high'
        elif any(word in text for word in medium_severity):
            severity = 'medium'
        
        print(f"🔍 Severity assessment for '{text}': {severity}")
        return severity

class RuleBasedClassifier:
    """
    Rule-based complaint classification as fallback.
    """
    
    def __init__(self):
        self.category_keywords = {
            'garbage': [
                'garbage', 'trash', 'waste', 'litter', 'rubbish', 'dump', 'bin', 'cleanup',
                'sanitation', 'hygiene', 'smell', 'odor', 'overflow', 'collection'
            ],
            'road': [
                'road', 'street', 'pothole', 'pavement', 'asphalt', 'crack', 'damage',
                'repair', 'construction', 'maintenance', 'surface', 'bump', 'hole'
            ],
            'streetlight': [
                'streetlight', 'street light', 'lamp', 'lamp post', 'lighting', 'dark',
                'broken light', 'flickering', 'outage', 'bulb', 'electricity', 'pole'
            ],
            'water': [
                'water', 'sewage', 'drain', 'pipe', 'leak', 'flood', 'overflow',
                'blockage', 'clogged', 'backup', 'smell', 'contamination'
            ],
            'noise': [
                'noise', 'loud', 'sound', 'disturbance', 'construction', 'traffic',
                'music', 'party', 'machinery', 'drilling', 'hammering'
            ],
            'traffic': [
                'traffic', 'congestion', 'signal', 'stop light', 'crossing', 'speed',
                'parking', 'vehicle', 'accident', 'jam', 'flow'
            ]
        }
    
    def classify_complaint(self, title: str, description: str) -> Tuple[str, float]:
        """Classify complaint using keyword matching"""
        text = f"{title} {description}".lower()
        
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[category] = score
        
        if not any(category_scores.values()):
            print(f"🔍 No keywords matched for '{text}', defaulting to 'other'")
            return 'other', 0.0
        
        best_category = max(category_scores, key=category_scores.get)
        max_score = max(category_scores.values())
        confidence = min(max_score / len(self.category_keywords[best_category]), 1.0)
        
        print(f"🔍 Category classification for '{text}': {best_category} (confidence: {confidence:.1%})")
        return best_category, confidence
    
    def get_category_details(self, category: str) -> dict:
        """Get category information"""
        category_details = {
            'garbage': {
                'display_name': 'Garbage & Waste',
                'priority': 'medium',
                'resolution_time': '1-2 days',
                'department': 'Waste Management',
                'actions': [
                    'Schedule immediate cleanup',
                    'Install additional bins if needed',
                    'Increase collection frequency',
                    'Investigate source of waste'
                ]
            },
            'road': {
                'display_name': 'Road & Infrastructure',
                'priority': 'high',
                'resolution_time': '1-3 weeks',
                'department': 'Public Works',
                'actions': [
                    'Inspect road damage',
                    'Schedule repair work',
                    'Install temporary warning signs',
                    'Assess structural integrity'
                ]
            },
            'streetlight': {
                'display_name': 'Street Lighting',
                'priority': 'medium',
                'resolution_time': '2-5 days',
                'department': 'Electrical Services',
                'actions': [
                    'Check electrical connections',
                    'Replace faulty bulbs',
                    'Update lighting infrastructure',
                    'Test automatic controls'
                ]
            },
            'water': {
                'display_name': 'Water & Sewage',
                'priority': 'high',
                'resolution_time': '1-7 days',
                'department': 'Water & Sewage',
                'actions': [
                    'Inspect water lines',
                    'Contact emergency services if severe',
                    'Schedule repair work',
                    'Monitor water quality'
                ]
            },
            'noise': {
                'display_name': 'Noise Pollution',
                'priority': 'low',
                'resolution_time': '1-3 days',
                'department': 'Code Enforcement',
                'actions': [
                    'Investigate noise source',
                    'Issue warnings if applicable',
                    'Monitor noise levels',
                    'Coordinate with local authorities'
                ]
            },
            'traffic': {
                'display_name': 'Traffic & Transportation',
                'priority': 'medium',
                'resolution_time': '1-2 weeks',
                'department': 'Traffic Management',
                'actions': [
                    'Analyze traffic patterns',
                    'Adjust signal timings',
                    'Implement traffic management',
                    'Coordinate with police department'
                ]
            },
            'other': {
                'display_name': 'Other Issues',
                'priority': 'low',
                'resolution_time': '3-7 days',
                'department': 'General Services',
                'actions': [
                    'Review complaint details',
                    'Assign appropriate department',
                    'Follow up with citizen',
                    'Document for future reference'
                ]
            }
        }
        
        return category_details.get(category, category_details['other'])

# Legacy compatibility - keep the old class names
ComplaintClassifier = RuleBasedClassifier
EnhancedComplaintAnalyzer = GeminiProAnalyzer


