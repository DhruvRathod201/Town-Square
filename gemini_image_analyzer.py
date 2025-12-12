#!/usr/bin/env python3
"""
Google Gemini Pro Image Analyzer for TownSquare
Much simpler and more powerful than Hugging Face API
"""

import os
import google.generativeai as genai
from PIL import Image
import json

# Configure Gemini Pro
GOOGLE_API_KEY = "AIzaSyDSIKPs1OoxtnvCTaZW-z0QJG0Gnw16rXI"  # Get from https://makersuite.google.com/app/apikey
genai.configure(api_key=GOOGLE_API_KEY)

class GeminiImageAnalyzer:
    """
    Simple and powerful image analyzer using Google Gemini Pro
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro-vision')
        
        # Complaint categories
        self.categories = {
            'road': 'Road & Infrastructure Issues',
            'water': 'Water & Pipe Problems', 
            'streetlight': 'Street Lighting Issues',
            'traffic': 'Traffic & Signal Problems',
            'garbage': 'Garbage & Waste Issues',
            'noise': 'Construction & Noise Problems'
        }
    
    def analyze_image(self, image_path: str) -> dict:
        """
        Analyze image using Gemini Pro Vision
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Create prompt for complaint analysis
            prompt = """
            Analyze this image as a civic complaint submission. Provide:
            
            1. **Category**: Choose from: Road, Water, Streetlight, Traffic, Garbage, Noise, or Other
            2. **Description**: What you see in the image
            3. **Severity**: Low, Medium, or High based on safety risk
            4. **Priority**: Low, Medium, or High based on urgency
            5. **Recommended Actions**: 3-4 specific actions city officials should take
            
            Format your response as JSON:
            {
                "category": "category_name",
                "description": "detailed description",
                "severity": "severity_level", 
                "priority": "priority_level",
                "recommended_actions": ["action1", "action2", "action3"],
                "confidence": "high/medium/low"
            }
            """
            
            # Get Gemini's analysis
            response = self.model.generate_content([prompt, image])
            
            # Parse response
            try:
                # Extract JSON from response
                response_text = response.text
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start != -1 and json_end != -1:
                    json_str = response_text[json_start:json_end]
                    analysis = json.loads(json_str)
                else:
                    # Fallback parsing
                    analysis = self._parse_fallback_response(response_text)
                
                return {
                    'success': True,
                    'filename': os.path.basename(image_path),
                    'gemini_response': response_text,
                    'parsed_analysis': analysis
                }
                
            except json.JSONDecodeError:
                # If JSON parsing fails, use fallback
                analysis = self._parse_fallback_response(response.text)
                return {
                    'success': True,
                    'filename': os.path.basename(image_path),
                    'gemini_response': response.text,
                    'parsed_analysis': analysis
                }
                
        except Exception as e:
            return {
                'success': False,
                'filename': os.path.basename(image_path),
                'error': str(e)
            }
    
    def _parse_fallback_response(self, response_text: str) -> dict:
        """
        Fallback parsing if JSON extraction fails
        """
        response_lower = response_text.lower()
        
        # Determine category from response
        category = 'other'
        if any(word in response_lower for word in ['road', 'pothole', 'street', 'asphalt']):
            category = 'road'
        elif any(word in response_lower for word in ['water', 'pipe', 'leak', 'flood']):
            category = 'water'
        elif any(word in response_lower for word in ['light', 'lamp', 'bulb', 'electrical', 'pole']):
            category = 'streetlight'
        elif any(word in response_lower for word in ['traffic', 'signal', 'vehicle']):
            category = 'traffic'
        elif any(word in response_lower for word in ['garbage', 'trash', 'waste']):
            category = 'garbage'
        elif any(word in response_lower for word in ['construction', 'noise', 'machinery']):
            category = 'noise'
        
        # Determine severity
        severity = 'medium'
        if any(word in response_lower for word in ['dangerous', 'critical', 'emergency', 'hazard']):
            severity = 'high'
        elif any(word in response_lower for word in ['minor', 'small', 'low']):
            severity = 'low'
        
        return {
            'category': category,
            'description': response_text[:200] + '...' if len(response_text) > 200 else response_text,
            'severity': severity,
            'priority': 'high' if severity == 'high' else 'medium',
            'recommended_actions': [
                'Inspect the reported issue',
                'Assess safety risks',
                'Schedule appropriate repairs',
                'Monitor the situation'
            ],
            'confidence': 'medium'
        }

def test_gemini_analyzer():
    """
    Test the Gemini analyzer
    """
    print("🚀 Testing Google Gemini Pro Image Analyzer")
    print("=" * 60)
    
    # Check if API key is set
    if GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("❌ Please set your Gemini API key first!")
        print("1. Go to https://makersuite.google.com/app/apikey")
        print("2. Create an API key")
        print("3. Replace 'YOUR_GEMINI_API_KEY_HERE' in the script")
        return
    
    # Initialize analyzer
    analyzer = GeminiImageAnalyzer()
    
    # Test with image.png
    image_path = "test_images/image.png"
    
    if os.path.exists(image_path):
        print(f"🔍 Analyzing: {image_path}")
        print("-" * 40)
        
        # Analyze image
        result = analyzer.analyze_image(image_path)
        
        if result['success']:
            print("✅ Analysis successful!")
            print("\n📊 **Gemini Pro Analysis Results:**")
            
            analysis = result['parsed_analysis']
            print(f"   • Category: {analysis['category'].title()}")
            print(f"   • Severity: {analysis['severity']}")
            print(f"   • Priority: {analysis['priority']}")
            print(f"   • Confidence: {analysis['confidence']}")
            
            print(f"\n📝 **Description:**")
            print(f"   {analysis['description']}")
            
            print(f"\n💡 **Recommended Actions:**")
            for i, action in enumerate(analysis['recommended_actions'], 1):
                print(f"   {i}. {action}")
                
        else:
            print(f"❌ Analysis failed: {result['error']}")
    else:
        print(f"❌ Image not found: {image_path}")
    
    print("\n" + "=" * 60)
    print("🎯 Gemini Pro Test Complete!")

if __name__ == "__main__":
    test_gemini_analyzer()


