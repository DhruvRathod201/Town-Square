# 🏘️ TownSquare - Complete Project Guide & Documentation (Part 1)

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Core Concepts Explained](#core-concepts-explained)
5. [Database Design](#database-design)

---

## 🎯 Project Overview

### What is TownSquare?
TownSquare is a **smart civic issue reporting platform** that helps citizens report community problems (like broken streetlights, potholes, garbage issues) and helps government officials manage and resolve them efficiently.

### Think of it like this:
- **Citizens** = People who report problems (like you reporting a broken streetlight)
- **Admins** = Government officials who fix the problems
- **AI** = A smart assistant that automatically categorizes and prioritizes complaints
- **System** = The digital platform that connects everyone

### Key Features:
- **User Registration & Authentication** - Secure account creation and login
- **AI-Powered Classification** - Automatic categorization of complaints
- **Image Upload & Analysis** - Photo-based complaint submission
- **Real-time Tracking** - Monitor complaint status from submission to resolution
- **Admin Dashboard** - Comprehensive complaint management for officials
- **Mobile-Responsive Design** - Works on all devices

---

## 🏗️ System Architecture

### High-Level Architecture Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (HTML/CSS/JS) │◄──►│   (Django)      │◄──►│   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Browser  │    │   AI Services   │    │   File Storage  │
│                 │    │   (Gemini Pro)  │    │   (Media)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### How Data Flows:
1. **User submits complaint** → Frontend sends data to Django
2. **Django processes** → Saves to database, calls AI service
3. **AI analyzes** → Categorizes and prioritizes the complaint
4. **Admin reviews** → Updates status and adds notes
5. **User tracks** → Sees updates in real-time

### Project Structure:
```
TownSquare/
├── complaints/                 # Main Django app
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── forms.py               # Form definitions
│   ├── admin.py               # Admin interface
│   ├── services.py            # AI classification service
│   └── urls.py                # URL routing
├── templates/                  # HTML templates
├── static/                     # CSS, JS, images
├── media/                      # User uploads
├── TownSquare/                 # Project settings
└── manage.py                   # Django management
```

---

## 🛠️ Technology Stack

### Backend Technologies
| Technology | Version | Purpose | Why We Use It |
|------------|---------|---------|---------------|
| **Django** | 5.2.4 | Web framework | Fast, secure, built-in admin |
| **Python** | 3.8+ | Programming language | Easy to learn, powerful |
| **SQLite** | Built-in | Database | Simple, no setup needed |

### AI & Machine Learning
| Technology | Purpose | How It Works |
|------------|---------|--------------|
| **Google Gemini Pro** | Image & text analysis | Analyzes photos and descriptions |
| **Rule-based Classifier** | Fallback classification | Uses keywords when AI fails |

### Frontend Technologies
| Technology | Purpose | Why We Use It |
|------------|---------|---------------|
| **Bootstrap 5** | UI framework | Responsive, mobile-friendly |
| **HTML5** | Structure | Semantic markup |
| **CSS3** | Styling | Custom design |
| **JavaScript** | Interactivity | Dynamic features |

### File Handling
| Technology | Purpose | Features |
|------------|---------|----------|
| **Pillow (PIL)** | Image processing | Resize, validate, optimize |
| **Django Media** | File storage | Organize uploads |

---

## 🧠 Core Concepts Explained

### 1. Django Framework (Simple Explanation)
**Think of Django like a smart restaurant:**
- **Kitchen (Backend)**: Where food is prepared (your code logic)
- **Dining Room (Frontend)**: Where customers sit (your website)
- **Menu (URLs)**: What customers can order (your pages)
- **Chef (Views)**: Who prepares the food (your functions)
- **Recipe Book (Models)**: How to make each dish (your data structure)

**Technical Explanation:**
Django is a **Model-View-Template (MVT)** framework:
- **Model**: Defines data structure and database relationships
- **View**: Contains business logic and handles requests
- **Template**: Renders HTML and presents data to users

### 2. Database Models (Simple Explanation)
**Think of models like forms you fill out:**
- **Citizen Model**: Like a contact form (name, phone, address)
- **Complaint Model**: Like a report form (problem, location, photo)
- **ComplaintUpdate Model**: Like a progress log (status changes, notes)

**Technical Explanation:**
Models are Python classes that inherit from `django.db.models.Model`:
- Each field becomes a database column
- Relationships (ForeignKey, OneToOneField) create table connections
- Methods can add custom behavior to data

### 3. AI Classification (Simple Explanation)
**Think of AI like a smart mail sorter:**
- **Input**: You show it a photo and describe a problem
- **Processing**: AI looks at the image and text
- **Output**: AI tells you what type of problem it is and how urgent

**Technical Explanation:**
The system uses **Google Gemini Pro Vision API**:
- **Image Analysis**: Processes uploaded photos
- **Text Analysis**: Analyzes complaint descriptions
- **Classification**: Categorizes into predefined types
- **Fallback**: Rule-based system when AI fails

---

## 🗄️ Database Design

### Database Schema Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      User       │    │     Citizen     │    │    Complaint    │
│                 │    │                 │    │                 │
│ • username      │◄──►│ • user (FK)     │◄──►│ • citizen (FK)  │
│ • email         │    │ • phone         │    │ • title         │
│ • password      │    │ • address       │    │ • description   │
│ • is_staff      │    │ • city          │    │ • location      │
│ • is_superuser  │    │ • state         │    │ • category      │
└─────────────────┘    └─────────────────┘    │ • image         │
                                              │ • status        │
                                              │ • severity      │
                                              │ • priority      │
                                              │ • admin_notes   │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ ComplaintUpdate │
                                              │                 │
                                              │ • complaint(FK) │
                                              │ • status        │
                                              │ • notes         │
                                              │ • updated_by(FK)│
                                              └─────────────────┘
```

### Model Relationships Explained

#### 1. User ↔ Citizen (One-to-One)
```python
# One user can have one citizen profile
user = models.OneToOneField(User, on_delete=models.CASCADE)
```
**What this means:**
- Each registered user gets exactly one citizen profile
- If user is deleted, citizen profile is also deleted
- Citizen profile stores additional info (phone, address, city)

#### 2. Citizen ↔ Complaint (One-to-Many)
```python
# One citizen can have many complaints
citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='complaints')
```
**What this means:**
- A citizen can submit multiple complaints
- Each complaint belongs to one citizen
- `related_name='complaints'` allows: `citizen.complaints.all()`

#### 3. Complaint ↔ ComplaintUpdate (One-to-Many)
```python
# One complaint can have many status updates
complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='updates')
```
**What this means:**
- Each complaint tracks its history
- Admins can add notes and status changes
- Creates a timeline of the complaint's progress

### Field Types & Choices

#### Status Choices
```python
STATUS_CHOICES = [
    ('pending', 'Pending'),        # Just submitted
    ('in_progress', 'In Progress'), # Being worked on
    ('resolved', 'Resolved'),      # Fixed!
    ('rejected', 'Rejected'),      # Cannot be fixed
]
```

#### Category Choices
```python
CATEGORY_CHOICES = [
    ('garbage', 'Garbage & Waste'),
    ('road', 'Road & Infrastructure'),
    ('streetlight', 'Street Lighting'),
    ('water', 'Water & Sewage'),
    ('noise', 'Noise Pollution'),
    ('traffic', 'Traffic & Transportation'),
    ('other', 'Other'),
]
```

### Key Model Methods

#### Complaint Model Methods
```python
def get_severity_display(self):
    """Get human-readable severity level."""
    return dict(self.SEVERITY_CHOICES).get(self.severity, 'Not Set')

def get_priority_display(self):
    """Get human-readable priority level."""
    return dict(self.PRIORITY_CHOICES).get(self.priority, 'Not Set')

def save(self, *args, **kwargs):
    # If status is being changed to resolved, set resolved_at
    if self.status == 'resolved' and not self.resolved_at:
        self.resolved_at = timezone.now()
    super().save(*args, **kwargs)
```

---

## 🔑 Key Takeaways from Part 1

1. **TownSquare is a civic issue reporting system** that connects citizens with government officials
2. **Django provides the framework** for building web applications with clean architecture
3. **AI integration** automatically categorizes and prioritizes complaints
4. **Database models** define the structure for users, citizens, complaints, and updates
5. **Relationships** between models create a connected data system

**Next in Part 2**: AI Integration, User Roles & Workflows, and Code Structure


