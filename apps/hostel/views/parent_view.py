from django.shortcuts import render
from django.views.generic import ListView
from apps.hostel.forms import StudentSignUpForm,StudentSignUpTwo, StudentSearchForm
from apps.hostel.models import User ,Student
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db.models import Q

# Create your views here.
class ParentHomeView(ListView):
    template_name = 'parent_view/parent_home.html'

    def get(self,request):
        return render(request,self.template_name)
