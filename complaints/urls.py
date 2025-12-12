from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # User pages (require login)
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path('ai-submit-complaint/', views.ai_complaint_submission, name='ai_complaint_submission'),
    path('get-location/', views.get_user_location, name='get_user_location'),
    path('complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    
    # Admin pages (require staff/admin)
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-complaint/<int:complaint_id>/', views.admin_complaint_detail, name='admin_complaint_detail'),
    
    # API endpoints
    path('api/complaint/<int:complaint_id>/update-status/', views.update_complaint_status, name='update_complaint_status'),
]


