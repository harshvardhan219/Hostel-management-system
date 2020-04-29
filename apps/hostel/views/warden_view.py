from django.shortcuts import render
from django.views.generic import ListView,TemplateView
from apps.hostel.forms import WardenSignUpForm,WardenSignUpTwo,RequestFormWarden,UserForm, ProfileForm, WardenSearchForm,NoticeFormWarden,RequestFormWarden
from apps.hostel.models import User ,Warden,HostelStaff, Noticee,Request
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from ..decorators import student_required, admin_required,hostelstaff_required,warden_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect

from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

@method_decorator([login_required], name='dispatch')
class WardenHomeView(ListView):
    model = HostelStaff
    #context_object_name = 'data'
    #template_name = 'warden_view/warden_home.html'
    def get(self,request):
        print(request.user)
        email = Warden.objects.get(user = request.user )
        #data=HostelStaff.objects.all()
        data=HostelStaff.objects.filter(hostel_name=email.hostel_name)
        return render(request,'warden_view/warden_home.html',{"data":data})


@login_required
@admin_required
def WardenSignUpView(request):
    if request.method == 'POST':
        main_form = WardenSignUpForm(request.POST)
        secondary_form = WardenSignUpTwo(request.user,request.POST)
        if main_form.is_valid() and secondary_form.is_valid():
            user = main_form.save()
            secondary_form.save(user)
            messages.success(request, 'New Warden Added  successfully')
            return redirect('admin_view:admin-home')
    else:
        main_form = WardenSignUpForm()
        secondary_form = WardenSignUpTwo(request.user)
    return render(request, 'admin_view/create_warden.html', {
        'main_form': main_form,
        'secondary_form': secondary_form
    })

class WardenProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'warden_view/profile.html'


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'warden_view/update-profile.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.warden)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('warden_view:warden-profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class WardenRequestView(ListView):
    model = Request
    context_object_name = 'list'
    template_name = 'warden_view/messages.html'
    def get_context_data(self,**kwargs):
        list= Request.objects.filter(users=self.request.user).order_by('issue_date')[::-1]
        print(self.request.user)
        return {'list':list}

def WardenUpdateSave(request):
    if request.method=='POST':
        form=ProfileForm(request.POST)
        warden=Warden()
        warden.user_id=form.data['user_id']
        warden.firstName=form.data['firstName']
        warden.lastName=form.data['lastName']
        warden.email=form.data['email']
        warden.phone_number=form.data['phone_number']
        warden.profile_image=form.data['profile_image']
        return HttpResponseRedirect('admin_view:admin-home')

def WardenUpdateView(request):
    warden=Warden.objects.get(user_id=request.GET['fieldid'])
    field={
            'profile_image':warden.profile_image,
            'firstName':warden.firstName,
            'lastName':warden.lastName,
            'hostel_name':warden.hostel_name,
            'email':warden.email,
            'phone_number':warden.phone_number,

    }
    form=ProfileForm(initial=field)
    data={'form':form,'warden':warden}
    res=render(request, 'admin_view/update_warden.html',data)
    return res

class WardenDeleteView(BSModalDeleteView):
    model = User
    context_object_name = 'field'
    template_name = 'admin_view/delete_warden.html'
    success_message = 'Success: Warden was deleted.'
    success_url = reverse_lazy('admin_view:admin-home')

class WardenReadView(BSModalReadView):
    model = Warden
    context_object_name = 'field'
    template_name = 'admin_view/read_warden.html'



def WardenSearchView(request):
    if request.method == 'POST':
        form=WardenSearchForm(request.POST)
        data=Warden.objects.filter(Q(firstName__icontains=form.data['search']) | Q(lastName__icontains=form.data['search']) | Q(hostel_name__icontains=form.data['search']))
        res=render(request,'admin_view/search_warden.html',{'form':form,'data':data})
        return res
    else:
        form=WardenSearchForm()
        res=render(request,'admin_view/search_warden.html',{'form':form})
        return res


##########################################################################################
def WardenCreateRequest(request):
    form = RequestFormWarden(request.user, request.POST or None)
    print("**form**")
    if request.method == 'POST':
        if form.is_valid():
            print('Saved notice')
            form.save(request.user)
            form = RequestFormWarden(request.user)
            return redirect("warden_view:sent-request")
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'warden_view/request.html',context)

def WardenCreateNotice(request):
    form = NoticeFormWarden(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            print('Saved notice')
            form.save(request.user)
            form = NoticeFormWarden(request.user)
            return redirect("warden_view:notice-warden2")
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'warden_view/notice.html',context)


class WardenNoticeList(ListView):
    model = Noticee
    context_object_name = 'noticee'
    template_name = 'warden_view/recieved_notice.html'
    def get_context_data(self,**kwargs):
        noticee = Noticee.objects.filter(users=self.request.user)[::-1]
        print(self.request.user)
        return {'noticee':noticee}


class WardenNoticeList2(ListView):
    model = Noticee
    context_object_name = 'noticee'
    template_name = 'warden_view/sent_notice.html'
    def get_context_data(self,**kwargs):
        noticee = Noticee.objects.filter(owner=self.request.user)[::-1]
        print(self.request.user)
        return {'noticee':noticee}

class WardenNoticficationView(ListView):
    model = Noticee
    context_object_name = 'noticee'
    template_name = 'warden_view/notification.html'
    def get_context_data(self,**kwargs):
        noticee = Noticee.objects.filter(users=self.request.user)[::-1]
        print(self.request.user)
        return {'noticee':noticee}



class WardenRequestList(ListView):
    model = Request
    context_object_name = 'note'
    template_name = 'warden_view/recieved_request.html'
    def get_context_data(self,**kwargs):
        note = Request.objects.filter(users=self.request.user)[::-1]
        print(self.request.user)
        return {'note':note}


class WardenRequestList2(ListView):
    model = Request
    context_object_name = 'note'
    template_name = 'warden_view/sent_request.html'
    def get_context_data(self,**kwargs):
        note = Request.objects.filter(owner=self.request.user)[::-1]
        print(self.request.user)
        return {'note':note}

class WardenNoticeReadView(BSModalReadView):
    model = Noticee
    context_object_name = 'field'
    template_name = 'warden_view/view-notice.html'

class WardenRequestReadView(BSModalReadView):
    model = Request
    context_object_name = 'field'
    template_name = 'warden_view/view-request.html'
