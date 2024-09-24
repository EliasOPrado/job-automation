from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.views import View
from .forms import ApplicationStatusForm
from core.models import JobApplication, Application
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm
from .forms import CustomUserChangeForm
from django.contrib.auth import logout, login

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
        form = CustomUserCreationForm()
        self.context['form'] = form
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        self.context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('signin-page')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")

        return render(request, self.template_name, self.context)

class SignInView(View):
        template_name = 'signin.html'
        context = {
            'page':'signin',
            'css_file':'sign_page.css'
            }

        def get(self, request):
            form = CustomAuthenticationForm()
            self.context['form'] = form
            return render(request, self.template_name, self.context)
        
        def post(self, request):
            form = CustomAuthenticationForm(request, data=request.POST)  # Pass request explicitly here
            self.context['form'] = form

            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('user-page')
            else:
                # Log form errors for debugging
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

            return render(request, self.template_name, self.context)
        
class SignOutView(View):
    def get(self, request):
        logout(request)
        messages.error(request, "You are logged out!")
        return redirect('signin-page')

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
        applications = Application.objects.filter(user=request.user).order_by("date_applied")
        paginator = Paginator(applications, per_page=10)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        self.context["page_object"] = page_object

        # time context
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())  # Monday
        start_of_month = today.replace(day=1)

        applications_today = Application.objects.filter(date_applied__date=today, user=request.user).count()
        applications_this_week = Application.objects.filter(date_applied__date__gte=start_of_week, user=request.user).count()
        applications_this_month = Application.objects.filter(date_applied__date__gte=start_of_month, user=request.user).count()

        # forms 
        application_status_form = ApplicationStatusForm()
        custom_user_change_form = CustomUserChangeForm(instance=request.user)

        # Remove the trailing commas
        self.context['application_status_form'] = application_status_form
        self.context['custom_user_change_form'] = custom_user_change_form
        self.context['count_applications'] = applications.count()
        self.context['applications_today'] = applications_today
        self.context['applications_this_week'] = applications_this_week
        self.context['applications_this_month'] = applications_this_month

        return render(request, self.template_name, self.context)
    
    def post(self, request):
        if 'change-user-form' in request.POST:
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('user-page')
            
        elif 'application-form' in request.POST:
            application_id = request.POST.get('application_id')
            application = get_object_or_404(Application, id=application_id, user=request.user)

            form = ApplicationStatusForm(request.POST, instance=application)
            if form.is_valid():
                form.save()
                return redirect('user-page')
            
        else:
            # Log form errors for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        # If the form is not valid, you might want to render the page again
        return self.get(request)