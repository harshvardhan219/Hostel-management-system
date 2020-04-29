from django.urls import path,include
from django.contrib.auth import views as auth_view
from .views import dashboard,admin_view,warden_view,staff_view,student_view,parent_view

urlpatterns = [
    path('',dashboard.home,name='home'),
    path('admin/', include(([
        path('admin-home',admin_view.AdminHomeView.as_view(),name='admin-home'),
        path('notice-list/',admin_view.AdminNoticeList.as_view(),name='notice-admin'),
        path('notice/',admin_view.AdminCreateNotice,name='create-notice'),
        path('request-list/',admin_view.adminRequestList.as_view(),name='request-list'),
        path('profile/', admin_view.AdminProfileView.as_view(), name='admin-profile'),
        path('profile-update/',admin_view.ProfileUpdateView.as_view(), name='profile-update'),
        path('notification/', admin_view.AdminNoticficationView, name='admin-notification'),
        path('request/', admin_view.adminRequestView.as_view(), name='admin-message'),
        path('read-notice/<int:pk>',admin_view.AdminNoticeReadView.as_view(), name='admin_read_notice'),
        path('read-request/<int:pk>',admin_view.AdminRequestReadView.as_view(), name='admin_read_request'),

    ], 'dashboard'),namespace='admin_view')),

    path('warden/', include(([
        path('warden-home/',warden_view.WardenHomeView.as_view(),name='warden-home'),
        path('search-warden/',warden_view.WardenSearchView,name='search-warden'),
        path('notice/',warden_view.WardenCreateNotice,name='create-notice'),
        path('notice-list/',warden_view.WardenNoticeList.as_view(),name='notice-warden'),
        path('sent-notice-list/',warden_view.WardenNoticeList2.as_view(),name='notice-warden2'),
        path('request/',warden_view.WardenCreateRequest,name='create-request-warden'),
        path('request-warden/',warden_view.WardenRequestList.as_view(),name='request-warden'),
        path('sent-request-list/',warden_view.WardenRequestList2.as_view(),name='sent-request'),
        path('profile/', warden_view.WardenProfileView.as_view(), name='warden-profile'),
        path('profile-update/',warden_view.ProfileUpdateView.as_view(), name='profile-update'),
        path('notification/', warden_view.WardenNoticficationView.as_view(), name='warden-notification'),
        path('messages/', warden_view.WardenRequestView.as_view(), name='warden-message'),
        path('update',warden_view.WardenUpdateView, name='update_warden'),
        path('update-save',warden_view.WardenUpdateSave, name='save_warden'),
        path('read/<int:pk>', warden_view.WardenReadView.as_view(), name='read_warden'),
        path('delete/<int:pk>',warden_view.WardenDeleteView.as_view(), name='delete_warden'),
        path('read-notice/<int:pk>',warden_view.WardenNoticeReadView.as_view(), name='warden_read_notice'),
        path('read-request/<int:pk>',warden_view.WardenRequestReadView.as_view(), name='warden_read_request'),


    ], 'dashboard'),namespace='warden_view')),

    path('staff/', include(([
        path('staff-home/',staff_view.StaffHomeView.as_view(),name='staff-home'),
        path('search-staff/',staff_view.StaffSearchView,name='search-staff'),
        path('profile/', staff_view.StaffProfileView.as_view(), name='staff-profile'),
        path('profile-update/',staff_view.ProfileUpdateView.as_view(), name='profile-update'),
        path('notification/',staff_view.StaffNoticficationView.as_view(), name='staff-notification'),
        path('messages/', staff_view.StaffRequestView, name='staff-message'),
        path('attendance/', staff_view.StudentAttendanceView, name='attendance'),

        path('notice/',staff_view.StaffCreateNotice,name='create-notice'),
        path('notice-list/',staff_view.StaffNoticeList.as_view(),name='notice-staff'),
        path('sent-notice-list/',staff_view.StaffNoticeList2.as_view(),name='notice-staff2'),
        path('request/',staff_view.StaffCreateRequest,name='create-request-staff'),
        path('request-staff/',staff_view.StaffRequestList.as_view(),name='request-staff'),
        path('sent-request-list/',staff_view.StaffRequestList2.as_view(),name='sent-request'),
        path('update',staff_view.StaffUpdateView, name='update_staff'),
        path('update-save',staff_view.StaffUpdateSave, name='save_staff'),
        path('read/<int:pk>', staff_view.StaffReadView.as_view(), name='read_staff'),
        path('delete/<int:pk>',staff_view.StaffDeleteView.as_view(), name='delete_staff'),


    ], 'dashboard'),namespace='staff_view')),

    path('student/', include(([
        path('student-home/',student_view.StudentHomeView.as_view(),name='student-home'),
        path('search-student/',student_view.StudentSearchView,name='search-student'),
        path('attendance/',student_view.StudentAttandanceView,name='student-attendance'),
        path('notification/',student_view.StudentNoticficationView.as_view(), name='student-notification'),
        path('messages/', student_view.StudentMessagesView, name='student-message'),
        path('profile/', student_view.StudentProfileView.as_view(), name='student-profile'),
        path('profile-update/',student_view.ProfileUpdateView.as_view(), name='profile-update'),

        path('attendance/', student_view.StudentAttandanceView, name='attendance'),

        path('notice-list/',student_view.StudentNoticeList.as_view(),name='notice-student'),
        path('request/',student_view.StudentCreateRequest,name='create-request-student'),
        path('sent-request-list/',student_view.StudentRequestList.as_view(),name='request-student'),

        path('update/<int:pk>',student_view.StudentUpdateView.as_view(), name='update_student'),
        path('read/<int:pk>', student_view.StudentReadView.as_view(), name='read_student'),
        path('delete/<int:pk>',student_view.StudentDeleteView.as_view(), name='delete_student'),

    ], 'dashboard'),namespace='student_view')),

    path('parent/', include(([
        path('parent-home/',parent_view.ParentHomeView.as_view(),name='parent-home'),
        ], 'dashboard'),namespace='parent_view')),



]
