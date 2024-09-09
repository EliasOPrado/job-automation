from django.shortcuts import render
from django.views import View

# Create your views here.
class HomeView(View):
    template_name = 'home.html'
    def get(self, request):
        return render(request, self.template_name)

class SignUpView(View):
    pass

class LoginView(View):
    pass

class JobListView(View):
    pass

class UserPageView(View):
    pass