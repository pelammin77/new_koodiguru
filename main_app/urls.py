



"""
URL configuration for koodiGuru project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.urls import path
from . import views
#from .views import CustomPasswordResetConfirmView
#from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import *
#from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

#from django.contrib.auth.views import *
#from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView

from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
app_name = "main_app"


urlpatterns = [
    
    #index url 

    path("", views.coming_soon, name="index"),
    path("start/", views.home, name="index"), 
    path('contact/', views.contact, name='contact'),
    path('blogi/', views.post_list, name='post_list'),
     path('blogi/<int:post_id>/', views.post_detail, name='post_detail'),

    path("profile/", views.profile, name="profile"),
    path("purchase_premium/", views.purchase_premium, name="purchase_premium"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("report/", views.report_view, name="raport tool"),
    path("password_change/", CustomPasswordChangeView.as_view(), name='password_change'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('tutorial/<int:tutorial_id>/', views.tutorial_detail, name='tutorial_detail'),
    path('perform_task/<int:task_id>/', views.perform_task, name='perform_task'),
    path('tasks/<int:task_id>/review/', views.review_task, name='review_task'),
    path('test-code/', views.test_code, name='test_code'),
    path('run-code-ano/', views.run_code_ano, name='run_code_ano'),
    path('add_course_to_user/<int:course_id>/', views.add_course_to_user, name='add_course_to_user'),
    path('remove_course/<int:course_id>/', views.remove_course_from_user, name='remove_course_from_user'),
    path('update-task-status-started/', views.update_task_status_started, name='update_task_status_started'),
    path('update-task-status-solved/', views.update_task_status_solved, name='update_task_status_solved'),
    path('save-code/', views.save_code, name='save_code'),
    path('save_editor_theme/', views.save_editor_theme, name='save_editor_theme'),
    path('search/', views.search, name='search'),
    path('send-email/', send_email, name='send_email'),
    #path('activate/<uidb64>/<token>/', views.activate_account, name='registration_confirm'),
    path('activate/<str:token>/', views.activate_account, name='registration_confirm'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



