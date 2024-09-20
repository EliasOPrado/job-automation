from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.views import View
from core.models import JobApplication, Application

# Create your views here.
class HomeView(View):
    template_name = 'home.html'
    context = {'css_file':'home_page.css'}
    def get(self, request):
        return render(request, self.template_name, self.context)

class SignUpView(View):
    template_name = 'signup.html'
    context = {
        'page':'signup',
        'css_file':'sign_page.css'
        }
    def get(self, request):
        return render(request, self.template_name, self.context)

class SignInView(View):
        template_name = 'signin.html'
        context = {
            'page':'signin',
            'css_file':'sign_page.css'
            }
        def get(self, request):
            return render(request, self.template_name, self.context)

class JobListView(View):
        template_name = 'job_list.html'
        context = {
            'page':'job_list',
            'css_file':'job_list_page.css',
            'job':JobApplication.objects.first()
            }
        def get(self, request, id=None):
            if id:
                job_position = get_object_or_404(JobApplication, pk=id)
                self.context["job"] = job_position
            
            query = request.GET.get('query', '')
        
            # Filter job positions based on the query
            if query:
                job_positions = JobApplication.objects.filter(job_title__icontains=query)
                if not job_positions.exists():  # Check if the queryset is empty
                    job_positions = JobApplication.objects.all()
                    messages.error(request, f"No results for query: '{query}'")
            else:
                job_positions = JobApplication.objects.all()
            
            self.context["jobs"] = job_positions
            return render(request, self.template_name, self.context)

class UserPageView(View):
    template_name = 'user.html'
    context = {
        'page':'user',
        'css_file':'user_page.css'
        }
    def get(self, request):
        applications = Application.objects.all().order_by("date_applied")
        paginator = Paginator(applications, per_page=5)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        self.context["page_object"] = page_object

        # time context
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())  # Monday
        start_of_month = today.replace(day=1)

        applications_today = Application.objects.filter(date_applied__date=today).count()
        applications_this_week = Application.objects.filter(date_applied__date__gte=start_of_week).count()
        applications_this_month = Application.objects.filter(date_applied__date__gte=start_of_month).count()

        # Remove the trailing commas
        self.context['applications_today'] = applications_today
        self.context['applications_this_week'] = applications_this_week
        self.context['applications_this_month'] = applications_this_month

        return render(request, self.template_name, self.context)