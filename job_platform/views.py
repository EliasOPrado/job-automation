from django.shortcuts import render
from django.views import View

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
    pass

class UserPageView(View):
    pass