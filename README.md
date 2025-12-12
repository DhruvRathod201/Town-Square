# 🏘️ TownSquare - Civic Issue Reporting Platform

A modern, AI-powered civic issue reporting and management system built with Django. TownSquare enables citizens to report community issues and helps government officials efficiently manage and resolve them.

## ✨ Features

### 👥 Citizen Features
- **User Registration & Authentication** - Secure account creation and login
- **Profile Management** - Update personal information and location details
- **Issue Submission** - Report civic problems with descriptions and photo uploads
- **AI-Powered Classification** - Automatic categorization of complaints
- **Real-time Tracking** - Monitor complaint status from submission to resolution
- **Dashboard** - View all submitted complaints and their progress

### 🛠️ Admin Features
- **Comprehensive Dashboard** - Overview of all complaints with statistics
- **Advanced Filtering** - Search and filter complaints by status, category, and location
- **Status Management** - Update complaint status with notes and tracking
- **Bulk Operations** - Efficiently manage multiple complaints
- **Analytics** - Category distribution and resolution metrics

### 🤖 AI Integration
- **Smart Classification** - Automatically categorize complaints using AI
- **Keyword Analysis** - Rule-based classification with machine learning capabilities
- **Hugging Face Ready** - Easy integration with external AI APIs
- **Confidence Scoring** - AI prediction confidence levels

## 🚀 Technology Stack

- **Backend**: Django 5.2 + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Bootstrap 5 + Custom CSS + JavaScript
- **AI/ML**: TensorFlow/Keras ready + Hugging Face API integration
- **File Handling**: Pillow for image processing
- **Authentication**: Django built-in user management

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd TownSquare
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
HUGGING_FACE_API_KEY=your-api-key-here
```

### AI Configuration
To use Hugging Face API for enhanced AI classification:

1. Get your API key from [Hugging Face](https://huggingface.co/)
2. Add it to your `.env` file
3. Update the classifier in `complaints/services.py`

## 📱 Usage

### For Citizens
1. **Register** - Create a new account
2. **Complete Profile** - Add location and contact information
3. **Submit Complaints** - Report issues with photos and descriptions
4. **Track Progress** - Monitor status updates in your dashboard

### For Administrators
1. **Access Admin Panel** - Use your superuser credentials
2. **Review Complaints** - View and categorize incoming issues
3. **Update Status** - Mark complaints as in progress or resolved
4. **Generate Reports** - Analyze complaint patterns and resolution times

## 🏗️ Project Structure

```
TownSquare/
├── complaints/                 # Main application
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── forms.py               # Form definitions
│   ├── admin.py               # Admin interface
│   ├── services.py            # AI classification service
│   └── urls.py                # URL routing
├── templates/                  # HTML templates
│   └── complaints/
│       ├── base.html          # Base template
│       ├── home.html          # Home page
│       ├── dashboard.html     # User dashboard
│       └── ...                # Other templates
├── static/                     # Static files
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript
│   └── images/                # Images
├── TownSquare/                 # Project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔒 Security Features

- **CSRF Protection** - Built-in Django security
- **User Authentication** - Secure login and session management
- **File Validation** - Image upload security checks
- **Role-based Access** - Admin-only functions protected
- **Input Sanitization** - XSS prevention

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in settings
2. Configure production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure HTTPS
5. Set secure `SECRET_KEY`

### Docker Deployment
```bash
# Build image
docker build -t townsquare .

# Run container
docker run -p 8000:8000 townsquare
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- **Mobile App** - Native iOS/Android applications
- **Advanced Analytics** - Machine learning insights
- **Integration APIs** - Connect with government systems
- **Real-time Notifications** - Push notifications for updates
- **Multi-language Support** - Internationalization
- **Advanced AI** - Image recognition and sentiment analysis

## 📊 Performance

- **Database Optimization** - Efficient queries and indexing
- **Caching** - Redis integration ready
- **CDN Ready** - Static file optimization
- **Responsive Design** - Mobile-first approach

---

**Built with ❤️ for better communities**



