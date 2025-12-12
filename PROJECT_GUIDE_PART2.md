# 🏘️ TownSquare - Complete Project Guide & Documentation (Part 2)

## 📋 Table of Contents
1. [AI Integration](#ai-integration)
2. [User Roles & Workflows](#user-roles--workflows)
3. [Code Structure & Functions](#code-structure--functions)
4. [Frontend & Templates](#frontend--templates)
5. [Security & Best Practices](#security--best-practices)

---

## 🤖 AI Integration

### AI Architecture Flow
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───►│  Gemini Pro     │───►│  AI Analysis    │
│                 │    │  Vision API     │    │  Results        │
│ • Text          │    │                 │    │                 │
│ • Image         │    │ • Image Analysis│    │ • Category      │
│ • Location      │    │ • Text Analysis │    │ • Severity      │
└─────────────────┘    └─────────────────┘    │ • Priority      │
                                              │ • Department    │
                                              │ • Timeline      │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │  Fallback      │
                                              │  Rule-Based    │
                                              │  Classifier    │
                                              └─────────────────┘
```

### How AI Analysis Works

#### 1. Gemini Pro Analysis
```python
def _analyze_with_gemini(self, title: str, description: str, image_path: str):
    """Analyze complaint using Gemini Pro Vision API."""
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
        """
        
        # Get Gemini's analysis
        response = self.model.generate_content([prompt, image])
        response_text = response.text
        
        # Parse JSON response and return results
        return self._parse_ai_response(response_text)
        
    except Exception as e:
        print(f"Gemini Pro API error: {e}")
        return self._fallback_analysis(title, description)
```

#### 2. Fallback Rule-Based Classification
```python
def classify_complaint(self, title: str, description: str) -> Tuple[str, float]:
    """Classify complaint using keyword matching"""
    text = f"{title} {description}".lower()
    
    category_scores = {}
    for category, keywords in self.category_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text)
        category_scores[category] = score
    
    if not any(category_scores.values()):
        return 'other', 0.0
    
    best_category = max(category_scores, key=category_scores.get)
    max_score = max(category_scores.values())
    confidence = min(max_score / len(self.category_keywords[best_category]), 1.0)
    
    return best_category, confidence
```

### AI Configuration
```python
# settings.py
GOOGLE_GEMINI_API_KEY = 'your-api-key-here'
HUGGINGFACE_API_KEY = 'your-backup-api-key'  # Backup option

# services.py
genai.configure(api_key=getattr(settings, 'GOOGLE_GEMINI_API_KEY', None))
self.model = genai.GenerativeModel('gemini-1.5-flash')
```

### AI Service Classes

#### GeminiProAnalyzer Class
```python
class GeminiProAnalyzer:
    """Primary AI analyzer using Google Gemini Pro Vision API."""
    
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
    
    def analyze_complaint(self, title: str, description: str, image_path: Optional[str] = None):
        """Main analysis method with fallback support."""
        if self.available and image_path:
            try:
                return self._analyze_with_gemini(title, description, image_path)
            except Exception as e:
                print(f"Gemini Pro analysis failed: {e}")
                return self._fallback_analysis(title, description)
        else:
            return self._fallback_analysis(title, description)
```

#### RuleBasedClassifier Class
```python
class RuleBasedClassifier:
    """Rule-based complaint classification as fallback."""
    
    def __init__(self):
        self.category_keywords = {
            'garbage': ['garbage', 'trash', 'waste', 'litter', 'rubbish'],
            'road': ['road', 'street', 'pothole', 'pavement', 'asphalt'],
            'streetlight': ['streetlight', 'street light', 'lamp', 'lighting'],
            'water': ['water', 'sewage', 'drain', 'pipe', 'leak'],
            'noise': ['noise', 'loud', 'sound', 'disturbance'],
            'traffic': ['traffic', 'congestion', 'signal', 'stop light']
        }
```

---

## 👥 User Roles & Workflows

### User Journey Flowchart
```
┌─────────────────┐
│   Home Page     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Register/Login │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Complete      │
│  Profile       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Dashboard      │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Submit          │
│ Complaint       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  AI Analysis    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Track Progress │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Resolution     │
└─────────────────┘
```

### Admin Workflow
```
┌─────────────────┐
│  Admin Login    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Dashboard      │
│  Overview       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Review         │
│  Complaints     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Update Status  │
│  & Add Notes    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Monitor        │
│  Progress       │
└─────────────────┘
```

### Role-Based Access Control

#### Citizen Permissions
- ✅ View own profile
- ✅ Submit complaints
- ✅ Track own complaints
- ✅ Update profile
- ❌ Access admin features
- ❌ View other users' complaints

#### Admin Permissions
- ✅ Access admin dashboard
- ✅ View all complaints
- ✅ Update complaint status
- ✅ Add admin notes
- ✅ Set severity/priority
- ✅ View statistics
- ❌ Submit complaints as citizen

### Permission Decorators
```python
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    """Check if user is admin/staff."""
    return user.is_staff or user.is_superuser

@login_required
def dashboard(request):
    """User dashboard view - requires login."""
    # Only logged-in users can access

@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard view - requires admin privileges."""
    # Only admin users can access
```

---

## 💻 Code Structure & Functions

### Key Functions Explained

#### 1. User Authentication Views

##### `register(request)` - User Registration
```python
def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()           # Create user account
            citizen = Citizen.objects.create(user=user)  # Create citizen profile
            login(request, user)         # Log user in
            messages.success(request, 'Registration successful!')
            return redirect('complaints:profile')
```
**What it does:**
- Handles user registration form
- Creates both User and Citizen records
- Automatically logs user in
- Redirects to profile completion

##### `user_login(request)` - User Login
```python
def user_login(request):
    """User login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('complaints:admin_dashboard')
            else:
                return redirect('complaints:dashboard')
```
**What it does:**
- Authenticates username/password
- Redirects admins to admin dashboard
- Redirects citizens to user dashboard

#### 2. Complaint Management Views

##### `submit_complaint(request)` - Submit New Complaint
```python
def submit_complaint(request):
    """Submit a new complaint."""
    if request.method == 'POST':
        if 'analyze_text' in request.POST:
            # Handle AI analysis request
            analyzer = GeminiProAnalyzer()
            analysis_results = analyzer.analyze_complaint(
                title, description, image
            )
            return JsonResponse(analysis_results)
        
        # Handle actual complaint submission
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.citizen = citizen
            
            # AI analysis and auto-categorization
            analyzer = GeminiProAnalyzer()
            analysis_results = analyzer.analyze_complaint(
                complaint.title, 
                complaint.description,
                request.FILES.get('image')
            )
            
            # Set AI-determined values
            complaint.category = analysis_results['category']
            complaint.severity = analysis_results['severity_level']
            complaint.priority = analysis_results['priority_level']
            complaint.save()
```
**What it does:**
- Handles both AI analysis and complaint submission
- Uses AI to automatically categorize complaints
- Sets severity and priority based on AI analysis
- Creates comprehensive admin notes

##### `admin_dashboard(request)` - Admin Overview
```python
def admin_dashboard(request):
    """Admin dashboard view."""
    # Get all complaints with filtering
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    
    complaints = Complaint.objects.all()
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if category_filter:
        complaints = complaints.filter(category=category_filter)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        complaints = complaints.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Statistics
    total_complaints = Complaint.objects.count()
    pending_count = Complaint.objects.filter(status='pending').count()
    resolved_count = Complaint.objects.filter(status='resolved').count()
```
**What it does:**
- Shows all complaints with filtering options
- Provides search functionality
- Displays statistics and counts
- Handles pagination for large datasets

#### 3. AI Service Functions

##### `GeminiProAnalyzer.analyze_complaint()` - AI Analysis
```python
def analyze_complaint(self, title: str, description: str, image_path: Optional[str] = None):
    """Analyze complaint using Gemini Pro Vision API."""
    if self.available and image_path:
        try:
            return self._analyze_with_gemini(title, description, image_path)
        except Exception as e:
            print(f"Gemini Pro analysis failed: {e}")
            return self._fallback_analysis(title, description)
    else:
        return self._fallback_analysis(title, description)
```
**What it does:**
- Attempts AI analysis first
- Falls back to rule-based if AI fails
- Handles both text and image analysis
- Returns structured analysis results

### Form Classes Explained

#### `UserRegistrationForm` - User Registration
```python
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
```
**What it does:**
- Extends Django's built-in user creation form
- Adds email, first name, last name fields
- Uses Bootstrap styling classes
- Validates email uniqueness

#### `ComplaintForm` - Complaint Submission
```python
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'location', 'image']
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size must be under 5MB.')
            
            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = image.name.lower()
            if not any(ext.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError('Please upload a valid image file.')
        
        return image
```
**What it does:**
- Creates complaint submission form
- Validates image file size and type
- Uses Bootstrap styling
- Ensures data quality

---

## 🎨 Frontend & Templates

### Template Inheritance Structure
```
base.html (Base template)
├── home.html (Home page)
├── login.html (Login form)
├── register.html (Registration form)
├── dashboard.html (User dashboard)
├── admin_dashboard.html (Admin dashboard)
├── submit_complaint.html (Complaint form)
├── complaint_detail.html (Complaint details)
└── profile.html (User profile)
```

### Base Template (`base.html`)
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}TownSquare{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <!-- Navigation items -->
    </nav>
    
    <!-- Main content -->
    <main class="container mt-4">
        <!-- Flash messages -->
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        <!-- Page content -->
        {% block content %}{% endblock %}
    </main>
    
    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
```

### Key Template Features

#### 1. Bootstrap Integration
- **Responsive Design**: Works on all device sizes
- **Component Library**: Pre-built UI components
- **Grid System**: Flexible layout system
- **Utility Classes**: Quick styling helpers

#### 2. Django Template Language
```html
<!-- Variable output -->
<h1>Welcome, {{ user.get_full_name|default:user.username }}!</h1>

<!-- Conditional statements -->
{% if user.is_authenticated %}
    <p>You are logged in!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}

<!-- Loops -->
{% for complaint in complaints %}
    <div class="complaint-item">
        <h3>{{ complaint.title }}</h3>
        <p>{{ complaint.description }}</p>
    </div>
{% empty %}
    <p>No complaints found.</p>
{% endfor %}

<!-- URL routing -->
<a href="{% url 'complaints:dashboard' %}">Dashboard</a>
```

### JavaScript Functionality

#### 1. AI Analysis Request
```javascript
function analyzeComplaint() {
    const formData = new FormData();
    formData.append('title', document.getElementById('id_title').value);
    formData.append('description', document.getElementById('id_description').value);
    formData.append('image', document.getElementById('id_image').files[0]);
    formData.append('analyze_text', 'true');
    
    fetch('/submit-complaint/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update form with AI results
            document.getElementById('id_category').value = data.category_code;
            // Show AI insights
            showAIResults(data);
        }
    });
}
```

#### 2. Geolocation
```javascript
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                
                // Send to Django backend
                fetch(`/get-location/?lat=${lat}&lng=${lng}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('id_location').value = data.location;
                        }
                    });
            },
            function(error) {
                console.error('Geolocation error:', error);
            }
        );
    }
}
```

---

## 🔒 Security & Best Practices

### Security Features Implemented

#### 1. CSRF Protection
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    # ... other middleware
]

# In templates
{% csrf_token %}

# In JavaScript
headers: {
    'X-CSRFToken': getCookie('csrftoken')
}
```
**What it prevents:**
- Cross-Site Request Forgery attacks
- Unauthorized form submissions
- Session hijacking

#### 2. User Authentication
```python
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def dashboard(request):
    """User dashboard view."""
    # Only logged-in users can access

@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard view."""
    # Only admin users can access
```
**What it prevents:**
- Unauthorized access to protected pages
- Privilege escalation
- Session hijacking

#### 3. File Upload Security
```python
def clean_image(self):
    image = self.cleaned_data.get('image')
    if image:
        # Check file size (5MB limit)
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Image file size must be under 5MB.')
        
        # Check file extension
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        ext = image.name.lower()
        if not any(ext.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError('Please upload a valid image file.')
    
    return image
```
**What it prevents:**
- Large file uploads (DoS attacks)
- Malicious file uploads
- Server storage abuse

### Best Practices Implemented

#### 1. Environment Variables
```python
# settings.py
SECRET_KEY = 'django-insecure-...'  # Should use environment variable
GOOGLE_GEMINI_API_KEY = 'your-api-key'  # Should use environment variable

# Better approach (create .env file):
from decouple import config

SECRET_KEY = config('SECRET_KEY')
GOOGLE_GEMINI_API_KEY = config('GOOGLE_GEMINI_API_KEY')
```

#### 2. Error Handling
```python
try:
    analysis_results = analyzer.analyze_complaint(title, description, image)
    if analysis_results['success']:
        return JsonResponse(analysis_results)
    else:
        return JsonResponse({'success': False, 'error': 'AI analysis failed'})
except Exception as e:
    return JsonResponse({'success': False, 'error': str(e)})
```
**What it provides:**
- Graceful error handling
- User-friendly error messages
- System stability

---

## 🔑 Key Takeaways from Part 2

1. **AI integration** uses Google Gemini Pro for smart complaint analysis with rule-based fallback
2. **User workflows** are clearly defined for both citizens and administrators
3. **Code structure** follows Django best practices with clean separation of concerns
4. **Frontend templates** use Bootstrap for responsive, mobile-friendly design
5. **Security measures** include CSRF protection, authentication, and file validation

**Next in Part 3**: Testing & Deployment, Troubleshooting, and Learning Resources


