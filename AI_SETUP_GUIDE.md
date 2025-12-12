# 🤖 AI Image Classification & Description Analysis Setup Guide

## 📋 **What You Get with This Implementation**

### **1. AI-Powered Features:**
- ✅ **Image Classification** - Automatically categorizes uploaded images
- ✅ **Image Description** - Generates natural language descriptions of images
- ✅ **Text Analysis** - Analyzes complaint text for better categorization
- ✅ **Severity Assessment** - Determines complaint severity level
- ✅ **Priority Scoring** - Calculates urgency and priority levels
- ✅ **Resolution Time Estimation** - Predicts how long resolution will take
- ✅ **Action Suggestions** - Recommends specific actions for each category

### **2. AI Models Used:**
- **Image Classification**: `microsoft/resnet-50`
- **Text Classification**: `distilbert-base-uncased`
- **Image Captioning**: `nlpconnect/vit-gpt2-image-captioning`
- **Text Generation**: `gpt2`

## 🚀 **Setup Instructions**

### **Step 1: Install Required Packages**
```bash
pip install transformers torch pillow requests python-decouple
```

### **Step 2: Get Hugging Face API Key**
1. Go to [Hugging Face](https://huggingface.co/)
2. Create an account (free)
3. Go to Settings → Access Tokens
4. Create a new token with "read" permissions
5. Copy the token

### **Step 3: Configure Environment Variables**
Create a `.env` file in your project root:
```env
HUGGINGFACE_API_KEY=your_api_key_here
DEBUG=True
SECRET_KEY=your_django_secret_key
```

### **Step 4: Update Django Settings**
Add to `TownSquare/settings.py`:
```python
from decouple import config

# Add this to your settings
HUGGINGFACE_API_KEY = config('HUGGINGFACE_API_KEY', default='')
```

### **Step 5: Test the AI Integration**
1. Start your Django server
2. Submit a complaint with an image
3. Check the admin notes for AI analysis results

## 🎯 **How It Works**

### **When a Complaint is Submitted:**
1. **Text Analysis**: AI analyzes the title and description
2. **Image Analysis** (if image provided):
   - Classifies the image content
   - Generates a description of what's in the image
3. **Combined Analysis**: Merges text and image insights
4. **Insights Generation**:
   - Severity level assessment
   - Priority calculation
   - Resolution time estimation
   - Action suggestions

### **Example AI Analysis Output:**
```
AI Analysis:
Severity: Medium
Priority: High
Estimated Resolution: 1-7 days
Image Description: A large pothole in the middle of the road with visible damage

Suggested Actions:
- Inspect water lines
- Contact emergency services if severe
- Schedule repair work
```

## 🔧 **Customization Options**

### **1. Change AI Models**
Edit `complaints/services.py`:
```python
self.models = {
    'image_classification': 'your-preferred-model',
    'text_classification': 'your-preferred-model',
    'image_captioning': 'your-preferred-model',
}
```

### **2. Add Custom Categories**
Update the `category_keywords` dictionary in `ComplaintClassifier`:
```python
self.category_keywords = {
    'your_category': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing categories
}
```

### **3. Customize Severity Assessment**
Modify the `_assess_severity` method in `AIComplaintAnalyzer`:
```python
def _assess_severity(self, title: str, description: str) -> str:
    # Add your custom severity logic here
    pass
```

## 🚨 **Important Notes**

### **1. API Rate Limits**
- Hugging Face free tier has rate limits
- For production, consider paid plans or self-hosted models

### **2. Fallback System**
- If AI analysis fails, the system falls back to rule-based classification
- No complaints will be lost due to AI failures

### **3. Privacy & Security**
- Images are processed through Hugging Face API
- Consider data privacy implications for your use case

## 🔄 **Alternative AI Services**

### **Option 1: Google Cloud Vision API**
```python
# Replace Hugging Face with Google Cloud Vision
from google.cloud import vision

def analyze_image_google_vision(image_path):
    client = vision.ImageAnnotatorClient()
    # Implementation here
```

### **Option 2: Azure Computer Vision**
```python
# Replace with Azure Computer Vision
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

def analyze_image_azure(image_path):
    client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
    # Implementation here
```

### **Option 3: AWS Rekognition**
```python
# Replace with AWS Rekognition
import boto3

def analyze_image_aws(image_path):
    client = boto3.client('rekognition')
    # Implementation here
```

## 📊 **Performance Optimization**

### **1. Caching**
```python
from django.core.cache import cache

def get_cached_analysis(complaint_id):
    cache_key = f"ai_analysis_{complaint_id}"
    return cache.get(cache_key)
```

### **2. Async Processing**
```python
from celery import shared_task

@shared_task
def analyze_complaint_async(complaint_id):
    # Run AI analysis in background
    pass
```

### **3. Batch Processing**
```python
def batch_analyze_complaints(complaint_ids):
    # Process multiple complaints together
    pass
```

## 🎉 **Next Steps**

1. **Test the AI integration** with sample complaints
2. **Monitor performance** and adjust models as needed
3. **Add more categories** specific to your use case
4. **Implement caching** for better performance
5. **Add user feedback** to improve AI accuracy

## 📞 **Support**

If you encounter issues:
1. Check your API key is correct
2. Verify internet connection
3. Check Hugging Face API status
4. Review error logs in Django console

---

**🎯 You now have a fully functional AI-powered complaint analysis system!**



