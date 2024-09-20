from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views import View
from core.models import JobApplication

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
            return render(request, self.template_name, self.context)