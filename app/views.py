from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.core.mail import send_mail
from .utils import send_otp_email, delete_old_otps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, OTP, Job, Profile
from .forms import JobForm, RegisterForm, LoginForm, ProfileForm,UserForm

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

def login_page(request):
    login_form = LoginForm()
    return render(request, 'login.html', {'login_form': login_form})

def logout_user(request):
    logout(request)
    return redirect('/')


def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'job_list.html', {'jobs': jobs})

def job_detail(request, id):
    try:
        job = Job.objects.get(id=id)
    except Job.DoesNotExist:
        return HttpResponse("Job not found", status=404)
    return render(request, 'job_details.html', {'job': job})

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
        
        # Check for the associated Profile object
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return HttpResponse("Profile not found", status=404)
    
        
        jobs = Job.objects.filter(is_active=True).order_by('-created_at')
        
        otp_entered = request.POST.get('otp')
        otp_record = OTP.objects.filter(user=user).last()

        # Check if OTP is correct
        if otp_record and otp_record.otp == otp_entered and otp_record.is_valid():
            login(request, user)
            context = {'user': user, 'jobs': jobs, 'profile': profile, 'user_form': user_form, 'profile_form': profile_form}
            return render(request, 'job_list.html', context)
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html')


def create_job(request):
    print('inside create-job')
    if request.method == "POST":
        jform = JobForm(request.POST,request.FILES)
        if jform.is_valid():
            job = jform.save(commit=False)
            job.save()
            return redirect('job_list')
    else:
        jform = JobForm()  # Initialize empty form for GET requests
        return render(request, 'home.html', {'job_form': jform})
       



def add_skills(request):
    if request.method == "POST":
        print("Adding skills")  # Check if this prints in your console
        skills = request.POST.getlist('skills')  # Get list of selected skills
        
        user_profile = request.user.profile  # Access user profile
        user_profile.skills= ", ".join(skills) # Store as comma-separated values
        user_profile.save()  # Save the model

        return render(request,'job_list.html',{'profile':user_profile})
    
    return JsonResponse({'message': 'Invalid request'})

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