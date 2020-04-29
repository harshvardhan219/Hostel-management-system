from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from apps.hostel.views import dashboard,admin_view,warden_view,staff_view,student_view,parent_view
from django.conf.urls import url
from django.contrib.auth import urls
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.hostel.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/admin/', admin_view.AdminSignUpView, name='admin_signup'),
    path('accounts/signup/warden/', warden_view.WardenSignUpView, name='warden_signup'),
    path('accounts/signup/staff/', staff_view.StaffSignUpView, name='staff_signup'),
    path('accounts/signup/student/',student_view.StudentSignUpView, name='student_signup'),

    path('change-password/',auth_views.PasswordChangeView.as_view(
            template_name='password.html',
            success_url='/'
        ),
        name='change-password'
    ),


]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
