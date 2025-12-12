from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Citizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.city or 'Unknown Location'}"

    class Meta:
        verbose_name = "Citizen"
        verbose_name_plural = "Citizens"

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    CATEGORY_CHOICES = [
        ('garbage', 'Garbage & Waste'),
        ('road', 'Road & Infrastructure'),
        ('streetlight', 'Street Lighting'),
        ('water', 'Water & Sewage'),
        ('noise', 'Noise Pollution'),
        ('traffic', 'Traffic & Transportation'),
        ('other', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=500)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    predicted_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to='complaints/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.citizen.user.username} ({self.get_status_display()})"
    
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
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"

class ComplaintUpdate(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='updates')
    status = models.CharField(max_length=20, choices=Complaint.STATUS_CHOICES)
    notes = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.complaint.title} - {self.get_status_display()} at {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Complaint Update"
        verbose_name_plural = "Complaint Updates"
