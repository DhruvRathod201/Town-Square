from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import json

from .models import Citizen, Complaint, ComplaintUpdate
from .forms import UserRegistrationForm, CitizenProfileForm, ComplaintForm, ComplaintStatusUpdateForm
from .services import RuleBasedClassifier, GeminiProAnalyzer

def is_admin(user):
    """Check if user is admin/staff."""
    return user.is_staff or user.is_superuser

def home(request):
    """Home page view."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('complaints:admin_dashboard')
        else:
            return redirect('complaints:dashboard')
    
    # Get some statistics for the home page
    total_complaints = Complaint.objects.count()
    resolved_complaints = Complaint.objects.filter(status='resolved').count()
    pending_complaints = Complaint.objects.filter(status='pending').count()
    
    context = {
        'total_complaints': total_complaints,
        'resolved_complaints': resolved_complaints,
        'pending_complaints': pending_complaints,
    }
    return render(request, 'complaints/home.html', context)

def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('complaints:admin_dashboard')
        else:
            return redirect('complaints:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create citizen profile
            citizen = Citizen.objects.create(user=user)
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('complaints:profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'complaints/register.html', {'form': form})

def user_login(request):
    """User login view."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('complaints:admin_dashboard')
        else:
            return redirect('complaints:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            if user.is_staff:
                return redirect('complaints:admin_dashboard')
            else:
                return redirect('complaints:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'complaints/login.html')

@login_required
def user_logout(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('complaints:home')

@login_required
def profile(request):
    """User profile view."""
    # Redirect admins to admin dashboard
    if request.user.is_staff:
        messages.warning(request, 'Admins should use the admin dashboard.')
        return redirect('complaints:admin_dashboard')
    
    try:
        citizen = request.user.citizen
    except Citizen.DoesNotExist:
        citizen = Citizen.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = CitizenProfileForm(request.POST, instance=citizen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('complaints:profile')
    else:
        form = CitizenProfileForm(instance=citizen)
    
    context = {
        'form': form,
        'citizen': citizen,
    }
    return render(request, 'complaints/profile.html', context)

@login_required
def dashboard(request):
    """User dashboard view."""
    # Redirect admins to admin dashboard
    if request.user.is_staff:
        messages.warning(request, 'Admins should use the admin dashboard.')
        return redirect('complaints:admin_dashboard')
    
    try:
        citizen = request.user.citizen
    except Citizen.DoesNotExist:
        citizen = Citizen.objects.create(user=request.user)
    
    # Get user's complaints
    complaints = Complaint.objects.filter(citizen=citizen).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(complaints, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_complaints = complaints.count()
    pending_complaints = complaints.filter(status='pending').count()
    in_progress_complaints = complaints.filter(status='in_progress').count()
    resolved_complaints = complaints.filter(status='resolved').count()
    
    context = {
        'page_obj': page_obj,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'in_progress_complaints': in_progress_complaints,
        'resolved_complaints': resolved_complaints,
    }
    return render(request, 'complaints/dashboard.html', context)

@login_required
def submit_complaint(request):
    """Submit a new complaint."""
    # Redirect admins to admin dashboard
    if request.user.is_staff:
        messages.warning(request, 'Admins cannot submit complaints. Use the admin dashboard to manage complaints.')
        return redirect('complaints:admin_dashboard')
    
    try:
        citizen = request.user.citizen
    except Citizen.DoesNotExist:
        citizen = Citizen.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Handle AI analysis request
        if 'analyze_text' in request.POST:
            title = request.POST.get('title', '')
            description = request.POST.get('description', '')
            image = request.FILES.get('image')
            
            if not title and not description:
                return JsonResponse({
                    'success': False,
                    'error': 'Please provide a title or description'
                })
            
            try:
                # Analyze with Gemini Pro
                analyzer = GeminiProAnalyzer()
                
                if image:
                    # Save image temporarily for analysis
                    import tempfile
                    import os
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                        for chunk in image.chunks():
                            tmp_file.write(chunk)
                        temp_image_path = tmp_file.name
                    
                    analysis_results = analyzer.analyze_complaint(title, description, temp_image_path)
                    os.unlink(temp_image_path)
                else:
                    analysis_results = analyzer.analyze_complaint(title, description)
                
                if analysis_results['success']:
                    return JsonResponse({
                        'success': True,
                        'category': analysis_results['category'].title(),
                        'category_code': analysis_results['category'],
                        'severity': analysis_results['severity_level'],
                        'priority': analysis_results['priority_level'],
                        'department': analysis_results['assigned_department'],
                        'resolution_time': analysis_results['estimated_resolution_time'],
                        'confidence': analysis_results['confidence'],
                        'insights': analysis_results['ai_insights']
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'AI analysis failed'
                    })
                    
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
        
        # Handle actual complaint submission
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.citizen = citizen
            
            # Enhanced AI analysis
            analyzer = GeminiProAnalyzer()
            
            analysis_results = analyzer.analyze_complaint(
                complaint.title, 
                complaint.description,
                request.FILES.get('image')
            )
            
            # Debug logging
            print(f"AI Analysis Results: {analysis_results}")
            print(f"Category: {analysis_results.get('category')}")
            print(f"Severity: {analysis_results.get('severity_level')}")
            print(f"Priority: {analysis_results.get('priority_level')}")
            
            # Set category and additional AI insights (AI values take precedence)
            complaint.category = analysis_results.get('category', 'other')
            complaint.predicted_category = analysis_results.get('category', 'other')
            
            # Auto-set severity and priority from AI analysis with fallbacks
            complaint.severity = analysis_results.get('severity_level', 'medium')
            complaint.priority = analysis_results.get('priority_level', 'medium')
            
            # Ensure values are valid
            if complaint.severity not in ['low', 'medium', 'high']:
                complaint.severity = 'medium'
            if complaint.priority not in ['low', 'medium', 'high']:
                complaint.priority = 'medium'
            
            print(f"Final values - Category: {complaint.category}, Severity: {complaint.severity}, Priority: {complaint.priority}")
            
            # Store comprehensive AI insights in admin_notes
            admin_notes = f"🤖 AI Analysis Report\n"
            admin_notes += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            admin_notes += f"📊 Classification Results:\n"
            admin_notes += f"• Category: {complaint.category.title()}\n"
            admin_notes += f"• Confidence: {analysis_results.get('confidence', 'medium')}\n"
            admin_notes += f"• Severity: {complaint.severity.title()}\n"
            admin_notes += f"• AI Provider: {analysis_results.get('ai_provider', 'Unknown')}\n\n"
            
            admin_notes += f"🎯 Priority & Timeline:\n"
            admin_notes += f"• Priority Level: {complaint.priority.title()}\n"
            admin_notes += f"• Estimated Resolution: {analysis_results.get('estimated_resolution_time', '1-2 weeks')}\n"
            admin_notes += f"• Assigned Department: {analysis_results.get('assigned_department', 'General Services')}\n\n"
            
            admin_notes += f"💡 Recommended Actions:\n"
            for i, action in enumerate(analysis_results['suggested_actions'], 1):
                admin_notes += f"{i}. {action}\n"
            
            admin_notes += f"\n🔍 AI Analysis Details:\n"
            admin_notes += f"• Analysis Method: {analysis_results['analysis_method']}\n"
            admin_notes += f"• AI Insights: {analysis_results['ai_insights']}\n"
            admin_notes += f"• Safety Concerns: {analysis_results['safety_concerns']}\n"
            
            complaint.admin_notes = admin_notes
            complaint.save()
            
            # Create initial status update
            ComplaintUpdate.objects.create(
                complaint=complaint,
                status='pending',
                notes='Complaint submitted and awaiting review.',
                updated_by=request.user
            )
            
            messages.success(request, 'Complaint submitted successfully with enhanced AI analysis! Our AI has analyzed your complaint and provided comprehensive insights.')
            return redirect('complaints:dashboard')
    else:
        form = ComplaintForm()
    
    return render(request, 'complaints/submit_complaint.html', {'form': form})

@login_required
def ai_complaint_submission(request):
    """
    New AI-powered complaint submission flow:
    1. User uploads image
    2. AI generates title, description, category
    3. Location auto-fetched
    4. User can edit all fields
    """
    if request.method == 'POST':
        if 'analyze_image' in request.POST:
            # Step 1: Analyze uploaded image with AI
            image = request.FILES.get('image')
            if image:
                # Save image temporarily
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    for chunk in image.chunks():
                        tmp_file.write(chunk)
                    temp_image_path = tmp_file.name
                
                try:
                    # Analyze with Gemini Pro
                    analyzer = GeminiProAnalyzer()
                    analysis = analyzer.analyze_complaint(
                        title="",  # Empty title for image-only analysis
                        description="",  # Empty description for image-only analysis
                        image_path=temp_image_path
                    )
                    
                    # Clean up temp file
                    os.unlink(temp_image_path)
                    
                    if analysis['success']:
                        # Return AI analysis as JSON
                        return JsonResponse({
                            'success': True,
                            'ai_title': f"{analysis['category'].title()} Issue",
                            'ai_description': analysis['description'],
                            'ai_category': analysis['category'],
                            'ai_severity': analysis['severity_level'],
                            'ai_priority': analysis['priority_level'],
                            'ai_department': analysis['assigned_department'],
                            'ai_confidence': analysis['confidence'],
                            'ai_insights': analysis['ai_insights']
                        })
                    else:
                        return JsonResponse({
                            'success': False,
                            'error': 'AI analysis failed'
                        })
                        
                except Exception as e:
                    # Clean up temp file
                    if os.path.exists(temp_image_path):
                        os.unlink(temp_image_path)
                    return JsonResponse({
                        'success': False,
                        'error': str(e)
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No image uploaded'
                })
        
        elif 'submit_complaint' in request.POST:
            # Step 2: Submit the final complaint
            form = ComplaintForm(request.POST, request.FILES)
            if form.is_valid():
                complaint = form.save(commit=False)
                complaint.citizen = request.user.citizen
                complaint.status = 'pending'
                
                # Run AI analysis on the final submission to ensure proper categorization
                analyzer = GeminiProAnalyzer()
                analysis_results = analyzer.analyze_complaint(
                    complaint.title, 
                    complaint.description,
                    request.FILES.get('image')
                )
                
                # Debug logging
                print(f"AI Analysis Results for AI submission: {analysis_results}")
                print(f"Category: {analysis_results.get('category')}")
                print(f"Severity: {analysis_results.get('severity_level')}")
                print(f"Priority: {analysis_results.get('priority_level')}")
                
                # Set AI analysis results
                complaint.category = analysis_results.get('category', 'other')
                complaint.predicted_category = analysis_results.get('category', 'other')
                complaint.severity = analysis_results.get('severity_level', 'medium')
                complaint.priority = analysis_results.get('priority_level', 'medium')
                
                # Ensure values are valid
                if complaint.severity not in ['low', 'medium', 'high']:
                    complaint.severity = 'medium'
                if complaint.priority not in ['low', 'medium', 'high']:
                    complaint.priority = 'medium'
                
                # Store comprehensive AI insights in admin_notes
                admin_notes = f"🤖 AI Analysis Report\n"
                admin_notes += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                admin_notes += f"📊 Classification Results:\n"
                admin_notes += f"• Category: {complaint.category.title()}\n"
                admin_notes += f"• Confidence: {analysis_results.get('confidence', 'medium')}\n"
                admin_notes += f"• Severity: {complaint.severity.title()}\n"
                admin_notes += f"• AI Provider: {analysis_results.get('ai_provider', 'Unknown')}\n\n"
                
                admin_notes += f"🎯 Priority & Timeline:\n"
                admin_notes += f"• Priority Level: {complaint.priority.title()}\n"
                admin_notes += f"• Estimated Resolution: {analysis_results.get('estimated_resolution_time', '1-2 weeks')}\n"
                admin_notes += f"• Assigned Department: {analysis_results.get('assigned_department', 'General Services')}\n\n"
                
                admin_notes += f"💡 Recommended Actions:\n"
                for i, action in enumerate(analysis_results.get('suggested_actions', []), 1):
                    admin_notes += f"{i}. {action}\n"
                
                admin_notes += f"\n🔍 AI Analysis Details:\n"
                admin_notes += f"• Analysis Method: {analysis_results.get('analysis_method', 'Unknown')}\n"
                admin_notes += f"• AI Insights: {analysis_results.get('ai_insights', 'No insights available')}\n"
                admin_notes += f"• Safety Concerns: {analysis_results.get('safety_concerns', 'No immediate safety concerns')}\n"
                
                complaint.admin_notes = admin_notes
                
                # Save the complaint with AI analysis
                complaint.save()
                
                # Create initial status update
                ComplaintUpdate.objects.create(
                    complaint=complaint,
                    status='pending',
                    notes='Complaint submitted successfully with AI analysis.',
                    updated_by=request.user
                )
                
                # Return JSON success instead of redirect for AJAX requests
                return JsonResponse({
                    'success': True,
                    'message': 'Complaint submitted successfully with AI analysis!',
                    'redirect_url': reverse('complaints:dashboard')
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
    
    return render(request, 'complaints/ai_complaint_submission.html')

@login_required
def get_user_location(request):
    """Get user's current location via JavaScript geolocation"""
    # This will be called by JavaScript with coordinates
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    
    if lat and lng:
        # You could use a reverse geocoding service here
        # For now, return coordinates
        location = f"Lat: {lat}, Lng: {lng}"
        return JsonResponse({
            'success': True,
            'location': location,
            'coordinates': {'lat': lat, 'lng': lng}
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Location not available'
    })

@login_required
def complaint_detail(request, complaint_id):
    """View complaint details."""
    # Redirect admins to admin complaint detail
    if request.user.is_staff:
        return redirect('complaints:admin_complaint_detail', complaint_id=complaint_id)
    
    complaint = get_object_or_404(Complaint, id=complaint_id, citizen=request.user.citizen)
    
    # Get status updates
    updates = ComplaintUpdate.objects.filter(complaint=complaint).order_by('-created_at')
    
    context = {
        'complaint': complaint,
        'updates': updates,
    }
    return render(request, 'complaints/complaint_detail.html', context)

@user_passes_test(is_admin)
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
            Q(location__icontains=search_query) |
            Q(citizen__user__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(complaints, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics (always show overall stats, not filtered)
    total_complaints = Complaint.objects.count()
    pending_count = Complaint.objects.filter(status='pending').count()
    in_progress_count = Complaint.objects.filter(status='in_progress').count()
    resolved_count = Complaint.objects.filter(status='resolved').count()
    
    # Category distribution (always show overall stats, not filtered)
    category_stats = Complaint.objects.values('category').annotate(count=Count('category')).order_by('-count')
    
    context = {
        'page_obj': page_obj,
        'total_complaints': total_complaints,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'category_stats': category_stats,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'search_query': search_query,
    }
    return render(request, 'complaints/admin_dashboard.html', context)

@user_passes_test(is_admin)
def admin_complaint_detail(request, complaint_id):
    """Admin view of complaint details."""
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        print(f"POST data: {request.POST}")  # Debug print
        form = ComplaintStatusUpdateForm(request.POST, instance=complaint)
        print(f"Form is valid: {form.is_valid()}")  # Debug print
        if form.is_valid():
            old_status = complaint.status
            new_status = form.cleaned_data['status']
            new_category = form.cleaned_data['category']
            admin_notes = form.cleaned_data['admin_notes']
            new_severity = form.cleaned_data.get('severity')
            new_priority = form.cleaned_data.get('priority')
            
            # Update complaint status, category, admin notes, severity, and priority
            complaint.status = new_status
            complaint.category = new_category
            complaint.admin_notes = admin_notes
            
            # Update severity and priority if provided
            if new_severity:
                complaint.severity = new_severity
            if new_priority:
                complaint.priority = new_priority
            
            # Set resolved_at if status is resolved
            if new_status == 'resolved' and old_status != 'resolved':
                complaint.resolved_at = timezone.now()
            
            complaint.save()
            
            # Create status update record
            ComplaintUpdate.objects.create(
                complaint=complaint,
                status=new_status,
                notes=form.cleaned_data.get('notes', ''),
                updated_by=request.user
            )
            
            # Create a more detailed success message
            status_msg = f'Status: {complaint.get_status_display()}'
            category_msg = f'Category: {complaint.get_category_display()}'
            severity_msg = f'Severity: {complaint.get_severity_display()}' if complaint.severity else ''
            priority_msg = f'Priority: {complaint.get_priority_display()}' if complaint.priority else ''
            
            message_parts = [status_msg, category_msg]
            if severity_msg:
                message_parts.append(severity_msg)
            if priority_msg:
                message_parts.append(priority_msg)
                
            messages.success(request, f'Complaint updated successfully! {", ".join(message_parts)}')
            return redirect('complaints:admin_complaint_detail', complaint_id=complaint.id)
        else:
            # Form validation failed
            messages.error(request, 'Please correct the errors below.')
            print(f"Form errors: {form.errors}")  # Debug print
    else:
        form = ComplaintStatusUpdateForm(instance=complaint)
        
        # Initialize form with complaint data including severity and priority
        initial_data = {
            'status': complaint.status,
            'category': complaint.category,
            'admin_notes': complaint.admin_notes,
            'severity': complaint.severity or 'low',
            'priority': complaint.priority or 'low'
        }
        form = ComplaintStatusUpdateForm(initial=initial_data)
    
    # Get status updates
    updates = ComplaintUpdate.objects.filter(complaint=complaint).order_by('-created_at')
    
    context = {
        'complaint': complaint,
        'form': form,
        'updates': updates,
    }
    return render(request, 'complaints/admin_complaint_detail.html', context)

@user_passes_test(is_admin)
@csrf_exempt
@require_http_methods(["POST"])
def update_complaint_status(request, complaint_id):
    """API endpoint to update complaint status."""
    try:
        data = json.loads(request.body)
        complaint = get_object_or_404(Complaint, id=complaint_id)
        
        new_status = data.get('status')
        notes = data.get('notes', '')
        
        if new_status not in dict(Complaint.STATUS_CHOICES):
            return JsonResponse({'error': 'Invalid status'}, status=400)
        
        complaint.status = new_status
        complaint.admin_notes = notes
        complaint.save()
        
        # Create status update record
        ComplaintUpdate.objects.create(
            complaint=complaint,
            status=new_status,
            notes=notes,
            updated_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'status': new_status,
            'status_display': complaint.get_status_display()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def about(request):
    """About page view."""
    return render(request, 'complaints/about.html')

def contact(request):
    """Contact page view."""
    return render(request, 'complaints/contact.html')
