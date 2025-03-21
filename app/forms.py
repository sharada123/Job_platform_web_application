from django import forms
from .models import Job,CustomUser,Profile,Education,Certification
class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','mobile_number','username','email','password','confirm_password','role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password again'}),
            'role': forms.Select(choices=CustomUser.ROLE_CHOICES, attrs={'class': 'form-control', 'placeholder': '-----------------'}),    
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email':forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        }
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','email_address','company','about_company','logo','vacancy_total','job_description','skills','required_education','location','min_salary','max_salary','job_type','office_time_from','office_time_to','employee_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name of company'}),
            'about_company': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About company'}),
            'vacancy_total': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '5'}),
            'logo':forms.ClearableFileInput(attrs={'class': 'form-control','placeholder': 'Logo'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job description'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter required skills'}),
            'required_education':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'add required education'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'min_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter minimum salary'}),
            'max_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter maximum salary'}),
            'job_type': forms.Select(choices=Job.job_type_choices, attrs={'class': 'form-control'}), 
            'employee_type':forms.Select(choices=Job.employee_type_choices, attrs={'class':'form-control'}),
            'office_time_from': forms.TimeInput(attrs={'type': 'time','step':'1'}),  # ✅ Use 'time' input type
            'office_time_to': forms.TimeInput(attrs={'type': 'time','step':'1'}),  # ✅ Use 'time' input type
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name', 'email','mobile_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile Number'}),
            
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Profile Picture'}),
           
        }

#educationform
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree','institution','passout_date','percentage']
        widgets = {
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Degree'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Institution'}),
            'percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Percentage'}),
            'passout_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','step':'1'}),  # ✅ Use 'date' input type
        }

#certificateform
class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['certification_name','institution','passout_date','certificate']
        widgets = {
            'certification_name': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Enter course name'}),
            'institution': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Enter Institution'}),
            'certificate': forms.ClearableFileInput(attrs={'class': 'form-control m-2', 'placeholder': 'upload Certificate'}),
            'passout_date': forms.DateInput(attrs={'class': 'form-control m-2', 'type': 'date','step':'1'}),  # ✅ Use 'date' input type
        }

#aboutform