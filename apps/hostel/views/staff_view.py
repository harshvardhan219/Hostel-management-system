from django.shortcuts import render
from django.views.generic import ListView,TemplateView
from apps.hostel.forms import StaffSignUpForm , StaffSignUpTwo,StaffSearchForm,NoticeFormStaff,RequestFormStaff,StaffUserForm,StaffProfileForm
from apps.hostel.models import User ,HostelStaff,Student,Noticee, Request
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
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
class StaffHomeView(LoginRequiredMixin,ListView):
    template_name = 'staff_view/staff_home.html'

    def get(self,request):
        data=Student.objects.all()
        print(self.request.user)
        return render(request,self.template_name,{"data":data})

class StaffProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_view/profile.html'


def StaffSignUpView(request):
    if request.method == 'POST':
        main_form = StaffSignUpForm(request.POST)
        secondary_form = StaffSignUpTwo(request.user,request.POST)
        if main_form.is_valid() and secondary_form.is_valid():
            user = main_form.save()
            # secondary_form.save(user)
            secondary_form.save(request.user)
            messages.success(request, 'New Staff Member Added  successfully')
            return redirect('warden_view:warden-home')
    else:
        main_form = StaffSignUpForm()
        secondary_form = StaffSignUpTwo(request.user)
    return render(request, 'warden_view/create_staff.html', {
        'main_form': main_form,
        'secondary_form': secondary_form
    })

def StaffUpdateSave(request):
    if request.method=='POST':
        form=StaffProfileForm(request.POST)
        hostelstaff=HostelStaff()
        hostelstaff.firstName=form.data['firstName']
        hostelstaff.lastName=form.data['lastName']
        hostelstaff.user_id=form.data['user_id']
        hostelstaff.email=form.data['email']
        hostelstaff.phone_number=form.data['phone_number']
        hostelstaff.profile_image=form.data['profile_image']
        return HttpResponseRedirect('warden_view:warden-home')

def StaffUpdateView(request):
    hostelstaff=HostelStaff.objects.get(user_id=request.GET['fieldid'])
    field={
            'profile_image':hostelstaff.profile_image,
            'firstName':hostelstaff.firstName,
            'lastName':hostelstaff.lastName,
            'hostel_name':hostelstaff.hostel_name,
            'email':hostelstaff.email,
            'phone_number':hostelstaff.phone_number,

    }
    form=StaffProfileForm(initial=field)
    data={'form':form,'hostelstaff':hostelstaff}
    res=render(request, 'warden_view/update_staff.html',data)
    return res


class StaffReadView(BSModalReadView):
    model = HostelStaff
    context_object_name = 'field'
    template_name = 'warden_view/detail_staff.html'


class StaffDeleteView(BSModalDeleteView):
    model = User
    context_object_name = 'field'
    template_name = 'warden_view/delete_staff.html'
    success_message = 'Success: Staff Member was deleted.'
    success_url = reverse_lazy('warden_view:warden-home')



def StaffRequestView(request):
    list = Request.objects.filter(users=self.request.user)[::-1]
    return render(request,'staff_view/messages.html',{'list':list})



class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = StaffUserForm
    profile_form = StaffProfileForm
    template_name = 'staff_view/update-profile.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = StaffUserForm(post_data, instance=request.user)
        profile_form = StaffProfileForm(post_data, file_data, instance=request.user.hostelstaff)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('staff_view:staff-profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



def StaffSearchView(request):
    if request.method == 'POST':
        form=StaffSearchForm(request.POST)

        data=HostelStaff.objects.filter(Q(firstName__icontains=form.data['search']) | Q(lastName__icontains=form.data['search']) | Q(hostel_name__icontains=form.data['search']))
        res=render(request,'warden_view/search_staff.html',{'form':form,'data':data})
        return res

    else:
        form=StaffSearchForm()
        res=render(request,'warden_view/search_staff.html',{'form':form})
        return res


def StaffCreateNotice(request):
    form = NoticeFormStaff(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            print('Saved notice')
            form.save(request.user)
            form = NoticeFormStaff(request.user)
            return redirect("staff_view:notice-staff2")
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'staff_view/notice.html',context)


class StaffNoticeList(ListView):
    model = Noticee
    context_object_name = 'noticee'
    template_name = 'staff_view/recieved_notice.html'
    def get_context_data(self,**kwargs):
        noticee = Noticee.objects.filter(users=self.request.user)[::-1]
        print(self.request.user)
        return {'noticee':noticee}


class StaffNoticeList2(ListView):
    model = Noticee
    context_object_name = 'noticee'
    template_name = 'staff_view/sent_notice.html'
    def get_context_data(self,**kwargs):
        noticee = Noticee.objects.filter(owner=self.request.user)[::-1]
        print(self.request.user)
        return {'noticee':noticee}

class StaffNoticficationView(ListView):
    model = Noticee
    context_object_name = 'noticee'
    template_name = 'staff_view/notification.html'
    def get_context_data(self,**kwargs):
        noticee = Noticee.objects.filter(users=self.request.user)[::-1]
        print(self.request.user)
        return {'noticee':noticee}


def StaffCreateRequest(request):
    form = RequestFormStaff(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            print('Saved notice')
            form.save(request.user)
            form = RequestFormStaff(request.user)
            return redirect("staff_view:sent-request")
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'staff_view/request.html',context)


# def StaffRequestList(request):
# #    note = Request.objects.filter()
# #    context = {
# #        'note': note
# #    }
#     return render(request, 'staff_view/recieved_request.html')

class StaffRequestList(ListView):
    model = Request
    context_object_name = 'note'
    template_name = 'staff_view/recieved_request.html'
    def get_context_data(self,**kwargs):
        note = Request.objects.filter(users=self.request.user)[::-1]
        print(self.request.user)
        return {'note':note}


class StaffRequestList2(ListView):
    model = Request
    context_object_name = 'note'
    template_name = 'staff_view/sent_request.html'
    def get_context_data(self,**kwargs):
        note = Request.objects.filter(owner=self.request.user)[::-1]
        print(self.request.user)
        return {'note':note}

##########################################################################################

def StudentAttendanceView(request):
    return render(request, 'staff_view/Attendance.html')
