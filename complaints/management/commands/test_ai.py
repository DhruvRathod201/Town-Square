from django.core.management.base import BaseCommand
from complaints.services import EnhancedComplaintAnalyzer
from django.conf import settings


class Command(BaseCommand):
    help = 'Test the AI complaint analysis system'

    def handle(self, *args, **options):
        self.stdout.write("🧪 Testing AI Complaint Analysis System...")
        self.stdout.write("=" * 60)
        
        # Check if API key is configured
        api_key = getattr(settings, 'HUGGINGFACE_API_KEY', None)
        if not api_key:
            self.stdout.write(self.style.ERROR("❌ No Hugging Face API key found in settings!"))
            return
        
        self.stdout.write(f"✅ API key found: {api_key[:10]}...")
        
        # Test the enhanced analyzer
        try:
            analyzer = EnhancedComplaintAnalyzer()
            self.stdout.write("✅ EnhancedComplaintAnalyzer initialized successfully")
            
            # Test text analysis
            test_title = "Large pothole in main street"
            test_description = "There is a dangerous pothole in the middle of the main street causing traffic issues and potential damage to vehicles."
            
            self.stdout.write(f"\n📝 Testing text analysis...")
            self.stdout.write(f"Title: {test_title}")
            self.stdout.write(f"Description: {test_description}")
            
            # Analyze the test complaint
            results = analyzer.analyze_complaint(test_title, test_description)
            
            self.stdout.write("\n📊 AI Analysis Results:")
            self.stdout.write(f"Category: {results['category']}")
            self.stdout.write(f"Confidence: {results['confidence']:.2f}")
            
            # Display AI insights
            insights = results.get('ai_insights', {})
            self.stdout.write(f"\n🔍 AI Insights:")
            self.stdout.write(f"Severity: {insights.get('severity_level', 'Unknown')}")
            self.stdout.write(f"Priority: {insights.get('priority_level', 'Unknown')}")
            self.stdout.write(f"Estimated Resolution: {insights.get('estimated_resolution_time', 'Unknown')}")
            
            # Display suggested actions
            actions = results.get('suggested_actions', [])
            if actions:
                self.stdout.write(f"\n💡 Suggested Actions:")
                for i, action in enumerate(actions, 1):
                    self.stdout.write(f"{i}. {action}")
            
            self.stdout.write("\n" + "=" * 60)
            self.stdout.write(self.style.SUCCESS("🎉 AI Integration Test Completed Successfully!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ AI Integration Test Failed: {e}"))
            self.stdout.write("Check your API key and internet connection.")
