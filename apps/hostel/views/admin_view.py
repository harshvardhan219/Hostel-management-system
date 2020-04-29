from django.shortcuts import render
from django.views.generic import ListView,TemplateView
from apps.hostel.forms import AdminSignUpForm,AdminSignUpTwo, WardenSearchForm,NoticeFormAdmin,AdminUserForm,AdminProfileForm
from apps.hostel.models import User ,Warden,Admin,Noticee,Request
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect

from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

def AdminSignUpView(request):
    if request.method == 'POST':
        print("**post***")
        main_form = AdminSignUpForm(request.POST)
        secondary_form = AdminSignUpTwo(request.POST)
        print("***end post***")
        if main_form.is_valid() and secondary_form.is_valid():
            print("***valid***")
            user = main_form.save()
            secondary_form.save(user)
            print("***end valid***")
            return redirect('admin_view:admin-home')
        else:
            print("not valid")
    else:
        main_form = AdminSignUpForm()
        secondary_form = AdminSignUpTwo(request.user)
    return render(request, 'admin_view/admin_signup.html', {
        'main_form': main_form,
        'secondary_form': secondary_form
    })


class AdminHomeView(ListView):
    template_name = 'admin_view/admin_home.html'

    def get(self,request):
        data=Warden.objects.all()
        print(self.request.user)
        return render(request,self.template_name,{"data":data})



def AdminNoticficationView(request):
    return render(request,'admin_view/notification.html')

class AdminProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_view/profile.html'

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
     user_form = AdminUserForm
     profile_form = AdminProfileForm
     template_name = 'admin_view/update-profile.html'

     def post(self, request):
         post_data = request.POST or None
         file_data = request.FILES or None

         user_form = AdminUserForm(post_data, instance=request.user)
         profile_form = AdminProfileForm(post_data, file_data, instance=request.user.admin)

         if user_form.is_valid() and profile_form.is_valid():
             user_form.save()
             profile_form.save()
             messages.error(request, 'Your profile is updated successfully!')
             return HttpResponseRedirect(reverse_lazy('admin_view:admin-profile'))

         context = self.get_context_data(
                                         user_form=user_form,
                                         profile_form=profile_form
                                     )

         return self.render_to_response(context)

     def get(self, request, *args, **kwargs):
         return self.post(request, *args, **kwargs)




def AdminCreateNotice(request):
    form = NoticeFormAdmin(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            messages.success(request, 'Notice Send successfully!')
            print('Saved notice')
            form.save(request.user)
            form = NoticeFormAdmin(request.user)
            return redirect("admin_view:notice-admin")
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'admin_view/notice.html',context)

class AdminNoticeList(ListView):
    model = Noticee
    context_object_name = 'note'
    template_name = 'admin_view/create_notice.html'
    def get_context_data(self,**kwargs):
        note = Noticee.objects.filter(owner=self.request.user)[::-1]
        print(self.request.user)
        return {'note':note}

class AdminNoticeReadView(BSModalReadView):
    model = Noticee
    context_object_name = 'field'
    template_name = 'admin_view/view-notice.html'


class adminRequestList(ListView):
    model = Request
    context_object_name = 'note'
    template_name = 'admin_view/request_list.html'
    def get_context_data(self,**kwargs):
        note = Request.objects.filter(users=self.request.user)[::-1]
        print(self.request.user)
        return {'note':note}


class adminRequestView(ListView):
    model = Request
    context_object_name = 'list'
    template_name = 'admin_view/messages.html'
    def get_context_data(self,**kwargs):
        list = Request.objects.filter(users=self.request.user)[::-1]
        print(self.request.user)
        return {'list':list}

class AdminRequestReadView(BSModalReadView):
    model = Request
    context_object_name = 'field'
    template_name = 'admin_view/view-request.html'
