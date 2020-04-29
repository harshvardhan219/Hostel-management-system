from django.shortcuts import redirect, render
from django.views.generic import TemplateView




def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('admin_view:admin-home')
        elif request.user.is_warden:
            return redirect('warden_view:warden-home')
        elif request.user.is_hostelstaff:
            return redirect('staff_view:staff-home')
        elif request.user.is_parent:
            return redirect('parent_view:parent-home')

        else:
            return redirect('student_view:student-home')
    return render(request, 'vkarma_landing.html')

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            
