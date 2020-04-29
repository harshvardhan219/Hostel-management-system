from django.shortcuts import render
from django.views.generic import ListView,TemplateView
from apps.hostel.forms import StudentSignUpForm,StudentSignUpTwo, StudentSearchForm,RequestFormStudent,StudentUserForm,StudentProfileForm
from apps.hostel.models import User ,Student,Noticee,Request
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from ..decorators import student_required, admin_required,hostelstaff_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

# Create your views here.

class StudentHomeView(ListView):
        model = Noticee
        context_object_name = 'note'
        template_name = 'student_view/student_home.html'
        def get_context_data(self,**kwargs):
            note = Noticee.objects.filter(users=self.request.user)[::-1]
            print(self.request.user)
            return {'note':note}


def StudentSignUpView(request):
    if request.method == 'POST':
        main_form = StudentSignUpForm(request.POST)
        secondary_form = StudentSignUpTwo(request.user,request.POST)
        if main_form.is_valid() and secondary_form.is_valid():
            user = main_form.save()
            secondary_form.save(request.user)
            return redirect('staff_view:staff-home')
    else:
        main_form = StudentSignUpForm()
        secondary_form = StudentSignUpTwo(request.user)
    return render(request, 'staff_view/create_student.html', {
        'main_form': main_form,
        'secondary_form': secondary_form
    })




class StudentUpdateView(BSModalUpdateView):
    model = Student
    template_name = 'staff_view/update_student.html'
    form_class = StudentSignUpTwo
    success_message = 'Success: Student was updated.'
    success_url = reverse_lazy('staff_view:staff-home')

class StudentDeleteView(BSModalDeleteView):
    model = User
    context_object_name = 'field'
    template_name = 'staff_view/delete_student.html'
    success_message = 'Success: Student was deleted.'
    success_url = reverse_lazy('staff_view:staff-home')

class StudentReadView(BSModalReadView):
    model = Student
    context_object_name = 'field'
    template_name = 'staff_view/detail_student.html'

def StudentSearchView(request):
    if request.method == 'POST':
        form=StudentSearchForm(request.POST)

        data=Student.objects.filter(Q(firstName__icontains=form.data['search']) | Q(lastName__icontains=form.data['search']) | Q(hostel_name__icontains=form.data['search']))
        res=render(request,'staff_view/search_student.html',{'form':form,'data':data})
        return res

    else:
        form=StudentSearchForm()
        res=render(request,'staff_view/search_student.html',{'form':form})
        return res

def StudentAttandanceView(request):
    res=render(request,'student_view/attendance.html')
    return res

class StudentProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'student_view/profile.html'

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = StudentUserForm
    profile_form = StudentProfileForm
    template_name = 'student_view/update-profile.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = StudentUserForm(post_data, instance=request.user)
        profile_form = StudentProfileForm(post_data, file_data, instance=request.user.student)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('student_view:student-profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)




def StudentCreateRequest(request):
    form = RequestFormStudent(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            print('Saved notice')
            form.save(request.user)
            form = RequestFormStudent(request.user)
            return redirect("student_view:request-student")
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'student_view/request.html',context)


def StudentMessagesView(request):
    return render(request,'student_view/messages.html')


class  StudentRequestList(ListView):
    model = Request
    context_object_name = 'note'
    template_name = 'student_view/request_list.html'
    def get_context_data(self,**kwargs):
        note = Request.objects.filter(owner=self.request.user)[::-1]
        print(self.request.user)
        return {'note':note}


class StudentNoticeList(ListView):
    model = Noticee
    context_object_name = 'note'
    template_name = 'student_view/notices.html'
    def get_context_data(self,**kwargs):
        note = Noticee.objects.filter(users=self.request.user)[::-1]
        print(self.request.user)
        return {'note':note}


class StudentNoticficationView(ListView):
    model = Noticee
    context_object_name = 'noticee'
    template_name = 'student_view/notification.html'
    def get_context_data(self,**kwargs):
        noticee = Noticee.objects.filter(users=self.request.user).order_by('issue_date')
        print(self.request.user)
        return {'noticee':noticee}
