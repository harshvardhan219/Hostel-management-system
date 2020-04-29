from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from crispy_forms.helper import FormHelper
from apps.hostel.models import  User,Warden,HostelStaff,Student,Noticee,Request,Admin
from bootstrap_modal_forms.forms import BSModalForm
import datetime
import time
import random
from django.db.models.fields import TimeField
from django.db.models import Q



class AdminSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(AdminSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ' username'
        self.fields['password1'].widget.attrs['placeholder'] = ' password'
        self.fields['password2'].widget.attrs['placeholder'] = ' confirm password'
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['username','password1', 'password2']:
            self.fields[fieldname].help_text = None


class AdminSignUpTwo(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ('firstName', 'lastName','email', 'phone_number', 'hostel_name','profile_image')

    def __init__(self, user, *args, **kwargs):
        super(AdminSignUpTwo, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs['placeholder'] = ' first name'
        self.fields['lastName'].widget.attrs['placeholder'] = ' last name'
        self.fields['hostel_name'].widget.attrs['placeholder'] = ' hostel name'
        self.fields['email'].widget.attrs['placeholder'] = ' email'
        self.fields['phone_number'].widget.attrs['placeholder'] = ' phone '
        self.fields['profile_image'].widget.attrs['placeholder'] = ' phone '

        self.helper = FormHelper()
        self.helper.form_show_labels = False


    def save(self, user):
        self.fields['user'] = user
        firstName = self.cleaned_data['firstName']
        lastName = self.cleaned_data['lastName']
        email = self.cleaned_data['email']
        phone_number = self.cleaned_data['phone_number']
        hostel_name = self.cleaned_data['hostel_name']
        profile_image = self.cleaned_data['profile_image']
        admin = Admin.objects.create(user=user,  email=email,firstName=firstName,lastName=lastName,
                                       phone_number=phone_number,hostel_name=hostel_name,profile_image=profile_image)


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
        ]
    def __init__(self, *args, **kwargs):
        super(AdminUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['username',]:
            self.fields[fieldname].help_text = None

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ('firstName', 'lastName','email', 'phone_number','profile_image')

    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)
        # self.fields['firstName'].widget.attrs['readonly'] = True
        # self.fields['lastName'].widget.attrs['readonly'] = True
        # self.fields['hostel_name'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['firstName','lastName','email','phone_number','profile_image']:
            self.fields[fieldname].help_text = None


class WardenSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def save(self):
        user = super().save(commit=False)
        user.is_warden = True
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(WardenSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ' username'
        self.fields['password1'].widget.attrs['placeholder'] = ' password'
        self.fields['password2'].widget.attrs['placeholder'] = ' confirm password'
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['username','password1', 'password2']:
            self.fields[fieldname].help_text = None


class WardenSignUpTwo(forms.ModelForm):
    class Meta:
        model = Warden
        fields = ('firstName', 'lastName','email', 'phone_number', 'hostel_name','profile_image')

    def __init__(self, user, *args, **kwargs):
        super(WardenSignUpTwo, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs['placeholder'] = ' first name'
        self.fields['lastName'].widget.attrs['placeholder'] = ' last name'
        self.fields['hostel_name'].widget.attrs['placeholder'] = ' hostel name'
        self.fields['email'].widget.attrs['placeholder'] = ' email'
        self.fields['phone_number'].widget.attrs['placeholder'] = ' phone '
        self.fields['profile_image'].widget.attrs['placeholder'] = ' phone '

        self.helper = FormHelper()
        self.helper.form_show_labels = False


    def save(self, user):
        self.fields['user'] = user
        firstName = self.cleaned_data['firstName']
        lastName = self.cleaned_data['lastName']
        email = self.cleaned_data['email']
        phone_number = self.cleaned_data['phone_number']
        hostel_name = self.cleaned_data['hostel_name']
        profile_image = self.cleaned_data['profile_image']
        warden = Warden.objects.create(user=user,  email=email,firstName=firstName,lastName=lastName,
                                       phone_number=phone_number,hostel_name=hostel_name,profile_image=profile_image)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
        ]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['username',]:
            self.fields[fieldname].help_text = None

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Warden
        fields = ('firstName', 'lastName','email', 'phone_number', 'hostel_name','profile_image')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs['readonly'] = True
        self.fields['lastName'].widget.attrs['readonly'] = True
        self.fields['hostel_name'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['firstName','lastName','email','phone_number','hostel_name','profile_image']:
            self.fields[fieldname].help_text = None


class WardenSearchForm(forms.Form):
     search = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': '  Enter warden name  or hostel name'}))


class StaffSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def save(self):
        user = super().save(commit=False)
        user.is_hostelstaff = True
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(StaffSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ' username'
        self.fields['password1'].widget.attrs['placeholder'] = ' password'
        self.fields['password2'].widget.attrs['placeholder'] = ' confirm password'
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['username','password1', 'password2']:
            self.fields[fieldname].help_text = None


class StaffSignUpTwo(forms.ModelForm):
    class Meta:
        model = HostelStaff
        fields = ('firstName', 'lastName','email', 'phone_number', 'hostel_name',)

    def __init__(self, user, *args, **kwargs):
        super(StaffSignUpTwo, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs['placeholder'] = ' first name'
        self.fields['lastName'].widget.attrs['placeholder'] = ' last name'
        self.fields['hostel_name'].widget.attrs['placeholder'] = ' hostel name'
        self.fields['email'].widget.attrs['placeholder'] = ' email'
        self.fields['phone_number'].widget.attrs['placeholder'] = ' phone '
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    @transaction.atomic
    def save(self, user):
    #    self.fields['user'] = user
        self.instance.user = user
        self.instance.warden = Warden.objects.get(user=user)
        return super().save()
        firstName = self.cleaned_data['firstName']
        lastName = self.cleaned_data['lastName']
        email = self.cleaned_data['email']
        phone_number = self.cleaned_data['phone_number']
        hostel_name = self.cleaned_data['hostel_name']
        hostelstaff = HostelStaff.objects.create(user=user,  email=email,firstName=firstName,lastName=lastName,
                                       phone_number=phone_number,hostel_name=hostel_name)


#    def save(self,user,commit=True):
#        obj = super().save(commit=False)
#        obj.warden=Warden.objects.get(user = user)
#        obj.save()
#        return obj

class StaffUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
        ]
    def __init__(self, *args, **kwargs):
        super(StaffUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['username',]:
            self.fields[fieldname].help_text = None

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = HostelStaff
        fields = ('firstName', 'lastName','email', 'phone_number', 'hostel_name','profile_image')

    def __init__(self, *args, **kwargs):
        super(StaffProfileForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs['readonly'] = True
        self.fields['lastName'].widget.attrs['readonly'] = True
        self.fields['hostel_name'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['firstName','lastName','email','phone_number','hostel_name','profile_image']:
            self.fields[fieldname].help_text = None



class StaffSearchForm(forms.Form):
     search = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': '  Enter staff name  or hostel name'}))


class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(StudentSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ' username'
        self.fields['password1'].widget.attrs['placeholder'] = ' password'
        self.fields['password2'].widget.attrs['placeholder'] = ' confirm password'
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['username','password1', 'password2']:
            self.fields[fieldname].help_text = None


class StudentSignUpTwo(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('firstName', 'lastName','email', 'phone_number', 'hostel_name','class_name','roll_number')

    def __init__(self, user, *args, **kwargs):
        super(StudentSignUpTwo, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs['placeholder'] = ' first name'
        self.fields['lastName'].widget.attrs['placeholder'] = ' last name'
        self.fields['hostel_name'].widget.attrs['placeholder'] = ' hostel name'
        self.fields['email'].widget.attrs['placeholder'] = ' email'
        self.fields['phone_number'].widget.attrs['placeholder'] = ' phone '
        self.fields['class_name'].widget.attrs['placeholder'] = ' class '
        self.fields['roll_number'].widget.attrs['placeholder'] = ' roll number '
        self.helper = FormHelper()
        self.helper.form_show_labels = False



    def save(self, user):
        # self.fields['user'] = user
        self.instance.user = user
        self.instance.hostelstaff, __ = HostelStaff.objects.get_or_create(user=user)
        return super().save()
        firstName = self.cleaned_data['firstName']
        lastName = self.cleaned_data['lastName']
        email = self.cleaned_data['email']
        phone_number = self.cleaned_data['phone_number']
        hostel_name  = self.cleaned_data['hostel_name']
        class_name   = self.cleaned_data['class_name']
        roll_number  = self.cleaned_data['roll_number']
        student = Student.objects.create(user=user,  email=email,firstName=firstName,lastName=lastName,
                                       phone_number=phone_number,hostel_name=hostel_name,class_name=class_name,roll_number=roll_number)

    # def save(self,pk,commit=True):
    #     obj = super().save(commit=False)
    #     obj.hostelstaff=HostelStaff.objects.first()
    #     obj.save()
    #     return obj


class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
        ]
    def __init__(self, *args, **kwargs):
        super(StudentUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['username',]:
            self.fields[fieldname].help_text = None

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('firstName', 'lastName','email', 'phone_number', 'hostel_name','profile_image','class_name','roll_number')

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs['readonly'] = True
        self.fields['lastName'].widget.attrs['readonly'] = True
        self.fields['hostel_name'].widget.attrs['readonly'] = True
        self.fields['class_name'].widget.attrs['readonly'] = True
        self.fields['roll_number'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for fieldname in ['firstName','lastName','email','phone_number','hostel_name','profile_image','class_name','roll_number']:
            self.fields[fieldname].help_text = None


class StudentSearchForm(forms.Form):
     search = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': '  Enter Student name  or hostel name'}))


class NoticeFormAdmin(forms.ModelForm):
    class Meta:
        model = Noticee
        fields = ('name','description','users','file',)

    def save(self,user):
        owner = user
        issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        users = self.cleaned_data['users']
        file = self.cleaned_data['file']

        Noticee.objects.create(name=name, description=description, users=users, file=file, owner=owner, issue_date=issue_date)

    def __init__(self, users, *args, **kwargs):
        super(NoticeFormAdmin, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.filter(is_warden=True).order_by('first_name')
        self.fields['name'].widget.attrs['placeholder'] = ' Subject'
        self.fields['file'].widget.attrs['placeholder'] = ' Subject'
        self.fields['description'].widget.attrs['placeholder'] = 'write your msg here . . .'
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class NoticeFormWarden(forms.ModelForm):
    class Meta:
        model = Noticee
        fields = ('name','description','users','file',)

    def save(self,user):
        owner = user
        issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        users = self.cleaned_data['users']
        file = self.cleaned_data['file']

        Noticee.objects.create(name=name, description=description, users=users, file=file, owner=owner, issue_date=issue_date)

    def __init__(self, users, *args, **kwargs):
        super(NoticeFormWarden, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.filter(is_hostelstaff=True)
        self.fields['name'].widget.attrs['placeholder'] = ' Subject'
        self.fields['file'].widget.attrs['placeholder'] = ' Subject'
        self.fields['description'].widget.attrs['placeholder'] = 'write your msg here . . .'
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class NoticeFormStaff(forms.ModelForm):
    class Meta:
        model = Noticee
        fields = ('name','description','users','file',)

    def save(self,user):
        owner = user
        issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        users = self.cleaned_data['users']
        file = self.cleaned_data['file']

        Noticee.objects.create(name=name, description=description, users=users, file=file, owner=owner, issue_date=issue_date)

    def __init__(self, users, *args, **kwargs):
        super(NoticeFormStaff, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.filter(is_student=True)
        self.fields['name'].widget.attrs['placeholder'] = ' Subject'
        self.fields['file'].widget.attrs['placeholder'] = ' Subject'
        self.fields['description'].widget.attrs['placeholder'] = 'write your msg here . . .'
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class RequestFormWarden(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('name','description','users','file',)

    def save(self,user):
        owner = user
        issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        users = self.cleaned_data['users']
        file = self.cleaned_data['file']

        Request.objects.create(name=name, description=description, users=users, file=file, owner=owner, issue_date=issue_date)

    def __init__(self, users, *args, **kwargs):
        super(RequestFormWarden, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.filter(is_admin=True)
        self.fields['name'].widget.attrs['placeholder'] = ' Subject'
        self.fields['file'].widget.attrs['placeholder'] = ' Subject'
        self.fields['description'].widget.attrs['placeholder'] = 'write your msg here . . .'
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class RequestFormStaff(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('name','description','users','file',)

    def save(self,user):
        owner = user
        issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        users = self.cleaned_data['users']
        file = self.cleaned_data['file']

        Request.objects.create(name=name, description=description, users=users, file=file, owner=owner, issue_date=issue_date)

    def __init__(self, users, *args, **kwargs):
        super(RequestFormStaff, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.filter(is_warden=True)
        self.fields['name'].widget.attrs['placeholder'] = ' Subject'
        self.fields['file'].widget.attrs['placeholder'] = ' Subject'
        self.fields['description'].widget.attrs['placeholder'] = 'write your msg here . . .'
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class RequestFormStudent(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('name','description','users','file',)

    def save(self,user):
        owner = user
        issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        users = self.cleaned_data['users']
        file = self.cleaned_data['file']

        Request.objects.create(name=name, description=description, users=users, file=file, owner=owner, issue_date=issue_date)

    def __init__(self, users, *args, **kwargs):
        super(RequestFormStudent, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.filter(is_hostelstaff=True)
        self.fields['name'].widget.attrs['placeholder'] = ' Subject'
        self.fields['file'].widget.attrs['placeholder'] = ' Subject'
        self.fields['description'].widget.attrs['placeholder'] = 'write your msg here . . .'
        self.helper = FormHelper()
        self.helper.form_show_labels = False
