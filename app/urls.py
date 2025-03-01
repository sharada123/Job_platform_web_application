from django.urls import path
from . import views
urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('create-job',views.create_job,name='create-job'),
    path('signup-page/',views.signup_page,name='signup'),
    path('register/',views.register,name='register'),
    path('login/',views.login_page,name='login_page'),
    path('logout/',views.logout_user,name='logout'),
    # path('view_profile_form/',views.view_profile_form, name='view_profile_form'),
    # path('view_resume/',views.view_resume, name='view_resume'),
    path('add_skills/' ,views.add_skills,name='add_skills'),
    path('upload_resume/',views.upload_resume, name='upload_resume'),
    path('add_about/',views.add_about, name='add_about'),
    path('update_profile/',views.update_profile, name='update_profile'),
    path("send-otp/", views.send_otp, name="send_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path('job-list/',views.job_list, name="job_list"),
    path('post_job/',views.create_job,name="post_job"),
    path('job_detail/<int:id>',views.job_detail, name="job_detail"),
    path('add_education',views.add_education, name="add_education"),
    path('add_certificate',views.add_certificate, name="add_certificate"),
]
