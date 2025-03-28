from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.core.mail import send_mail
from .utils import send_otp_email, delete_old_otps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, OTP, Job, Profile,Education,Certification,Application
from .forms import JobForm, RegisterForm, LoginForm, ProfileForm,UserForm,EducationForm,CertificationForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os
import zipfile
from django.core.files.storage import default_storage
def homepage(request):
    jform=JobForm()
    return render(request, 'home.html',{'job_form':jform})

def signup_page(request):
    signup_form = RegisterForm()
    return render(request, 'user_register.html', {'signup_form': signup_form})

def register(request):
    if request.method == 'POST':
        signup_form = RegisterForm(request.POST)
        login_form = LoginForm()
        if signup_form.is_valid():
            email = signup_form.cleaned_data['email']  # Use cleaned_data
            username = signup_form.cleaned_data['username']
            
            if CustomUser.objects.filter(Q(email=email) | Q(username=username)).exists():
                return render(request, 'user_register.html', {
                    'signup_form': signup_form,
                    'errmsg': 'User with this email or username already exists'
                })
            
            user = signup_form.save(commit=False)
            user.set_password(signup_form.cleaned_data['password'])
            user.save()
            return render(request, 'login.html', {'login_form': login_form})
        else:
            return render(request, 'user_register.html', {'signup_form': signup_form})
    else:
        signup_form = RegisterForm()  # Initialize empty form for GET requests
        return render(request, 'user_register.html', {'signup_form': signup_form})
@login_required
def employeer_dashboard(request):
    jform=JobForm()
    jobs=Job.objects.filter(user=request.user).order_by('-created_at')
    total_applications = request.session.get('total_applications', 0)  # Default to 0 if not found
    return render(request, 'job_provider_dashboard.html',{'job_form':jform,'jobs':jobs,'total_applications':total_applications})

def login_page(request):
    login_form = LoginForm()
    return render(request, 'login.html', {'login_form': login_form})

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def job_list(request):
    education_form=EducationForm()
    certification_form=CertificationForm()
    education=Education.objects.filter(user=request.user.id)
    certificate=Certification.objects.filter(user=request.user.id)
    # print(education)
    print(certificate)
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'job_list.html', {'jobs': jobs,'certification_form':certification_form,'education_form':education_form,'education':education,'certificate':certificate})

@login_required
def job_detail(request, id):
    try:
        job = Job.objects.get(id=id)
        application=Application.objects.filter(job=job.id,user=request.user)
        
    except Job.DoesNotExist:
        return HttpResponse("Job not found", status=404)
    if application:
        return render(request, 'job_details.html', {'job': job,'application':True})
    else:

        return render(request, 'job_details.html', {'job': job,'application':False})

# Store OTP in a dictionary (temporary)
otp_storage = {}

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        login_form = LoginForm()
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user using Django's built-in authentication
        user = authenticate(request, username=username, password=password)

        if user is not None and user.email == email:  # Ensure the email also matches
            send_otp_email(user)
            request.session['email'] = email
            return render(request, "verify_otp.html", {'message': f'OTP is sent to {email}'})
        else:
            return render(request, "login.html", {'message': 'Invalid credentials', 'login_form': login_form})

    return render(request, 'login.html', {'message': 'Invalid Request', 'login_form': login_form})

@csrf_exempt
def verify_otp(request):
    # Delete old OTPs
    delete_old_otps()

    if request.method == "POST":
        email = request.session.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return redirect('send_otp')

        education = Education.objects.filter(user=user)
        certificate = Certification.objects.filter(user=user)
        profile = Profile.objects.filter(user=user).first()  # Avoids crashing if profile is missing
        
        jobs = Job.objects.filter(is_active=True).order_by('-created_at')
        otp_entered = request.POST.get('otp')
        otp_record = OTP.objects.filter(user=user).order_by('-created_at').first()

        # Check if OTP is correct
        if otp_record and otp_record.otp == otp_entered and otp_record.is_valid():
            login(request, user)
            if user.role=='job_seeker':
                return redirect('job_list')
            elif user.role=='job_provider':
                jform=JobForm()
                return redirect('employeer_dashboard')
            else:
                return HttpResponse('No role specified')

        return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html')

@login_required
def create_job(request):
    print('inside create-job')
    if request.method == "POST":
        jform = JobForm(request.POST,request.FILES)
        if jform.is_valid():
            job = jform.save(commit=False)
            job.user = request.user  # Associate the job with the current user
            job.save()
            return redirect('employeer_dashboard')
    else:
        jform = JobForm()  # Initialize empty form for GET requests
        return redirect('employeer_dashboard')
       


@login_required
def add_skills(request):
    if request.method == "POST":
        print("Adding skills")  # Check if this prints in your console
        skills = request.POST.getlist('skills')  # Get list of selected skills
        
        user_profile = request.user.profile  # Access user profile
        user_profile.skills= ", ".join(skills) # Store as comma-separated values
        user_profile.save()  # Save the model

        return render(request,'job_list.html',{'profile':user_profile})
    
    return JsonResponse({'message': 'Invalid request'})

@login_required
def upload_resume(request):
    user_profile=request.user.profile
    jobs=Job.objects.filter(is_active=True).order_by('-created_at')
    if request.method == "POST" and request.FILES.get('resume'):
        resume=request.FILES.get('resume')
        print(resume)
       
        user_profile.resume=resume
        user_profile.save()  # Save the model
        return render(request,'job_list.html',{'profile':user_profile,'jobs':jobs})
    else:
     return render(request,'job_list.html',{'profile':user_profile,'jobs':jobs})

@login_required
def add_about(request):
    user_profile=request.user.profile
    jobs=Job.objects.filter(is_active=True).order_by('-created_at')
    if request.method == "POST":
        about=request.POST.get('about')
        user_profile.about_me=about
        user_profile.save()  # Save the model
        return render(request,'job_list.html',{'profile':user_profile,'jobs':jobs})
    else:

     return render(request,'job_list.html',{'profile':user_profile,'jobs':jobs})

@login_required
def add_education(request):
    if  request.method == 'POST':
        education_form =EducationForm(request.POST)
        if education_form.is_valid():
            education = education_form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('job_list')
        else:
            return render(request, 'job_list.html', {'education_form': education_form})
@login_required
def add_certificate(request):
    if  request.method == 'POST':
        certificate_form =CertificationForm(request.POST,request.FILES)
        if certificate_form.is_valid():
            certificate = certificate_form.save(commit=False)
            certificate.user = request.user
            certificate.save()
            return redirect('job_list')
        else:
            return render(request, 'job_list.html', {'certificate_form': certificate_form})
    
@login_required
def update_profile(request):
    # Get the currently logged-in user
    user = CustomUser.objects.get(email=request.user.email)
    jobs=Job.objects.filter(is_active=True).order_by('-created_at')
    try:
        # Get the associated profile
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return HttpResponse("Profile not found", status=404)

    if request.method == 'POST':
        # Get data from POST request
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        mob = request.POST.get('mob')
        pic = request.FILES.get('img')  # Profile picture (if uploaded)

        # Update the user fields
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.mobile_number = mob

        # If a new profile picture is uploaded, update it
        if pic:
            profile.profile_image = pic

        # Save the changes to the user and profile
        user.save()
        profile.save()

        # Redirect to a success page or profile page (you can modify this as needed)
        return redirect('job_list')  # Modify 'profile' to your success or profile URL

    # Render the template to update the profile (for GET request)
    return render(request, 'job_list.html', {'user': user, 'profile': profile,'jobs':jobs})


@login_required
def apply(request, job_id):
    job = Job.objects.get(id=job_id)
    profile = Profile.objects.get(user=request.user.id)
    resume = profile.resume
    recipient_email = job.email_address
    #one thing to insert record into application model for logged in user
    #1) check already applied user
    if Application.objects.filter(job=job, user=request.user).exists():
        return redirect('job_detail', id=job.id)
    else:
        # Create application object
        application = Application(job=job, user=request.user, resume=resume)
        application.save()

        # Create email message with attachment
        email = EmailMessage(
            subject=f"Job Application for role {job.title.upper()}",
            body=f'''Respected Sir/Ma'am,
            
                    My name is {request.user.first_name} {request.user.last_name}.  
                    I am interested in the position of {job.title.upper()}.  
                    Please find my attached resume below.  

                    Thank you!  
                    {request.user.first_name} {request.user.last_name}
                    ''',
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient_email],
        )

        # Ensure email body is treated as plain text
        email.content_subtype = "plain"
        # Attach resume if it exists
        if resume:
            resume_path = resume.path
            with open(resume_path, 'rb') as file:
                email.attach(resume.name, file.read(), 'application/pdf')

        # Send email
        email.send(fail_silently=True)

        return redirect('job_detail', id=job.id)
def all_applied_jobs(request):
    applied_jobs = Application.objects.filter(user=request.user).select_related('job')
    
    return render(request, 'applied_jobs.html', {'applied_jobs': applied_jobs})


def delete_job(request, job_id):
    delete_obj = get_object_or_404(Job, id=job_id)
    delete_obj.delete()
    messages.success(request, f"Job {delete_obj.title} deleted successfully!")
    return redirect('employeer_dashboard')

def view_all_applications(request,job_id):
    print('Function total_applications called')
    job=Job.objects.get(id=job_id)
    print(job)
    applications=Application.objects.filter(job=job)
    print(applications.count())
    print(applications[0].resume)
    return render(request, 'view_all_applications.html', {'job': job,'applications': applications})
    
def download_resume(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job)

    if not applications.exists():
        return HttpResponse("No resumes found for this job.", content_type="text/plain")

    zip_filename = f"resumes_{job.title.replace(' ', '_')}.zip"
    zip_path = os.path.join("media", zip_filename)

    # Create ZIP file
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for application in applications:
            if application.resume:
                resume_path = application.resume.path
                if os.path.exists(resume_path):
                    zipf.write(resume_path, os.path.basename(resume_path))

    # Serve the ZIP file
    with open(zip_path, "rb") as zipf:
        response = HttpResponse(zipf.read(), content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'
    
    # Delete the ZIP file after serving 
    os.remove(zip_path)

    return response