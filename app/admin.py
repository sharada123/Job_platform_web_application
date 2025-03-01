from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,OTP,Job,Profile,Application,Education,Certification

class CustomUserAdmin(UserAdmin):  # Inherit Django's default UserAdmin
    model = CustomUser
    list_display = ('first_name','last_name','mobile_number','username', 'email', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (  # Add custom fields to admin panel
        ('Additional Info', {'fields': ('role','confirm_password','mobile_number')}),
    )

class EducationAdmin(admin.ModelAdmin):
    model = Education
    list_display=('user','institution','degree','percentage','passout_date')

class CertificationAdmin(admin.ModelAdmin):
    model = Certification
    list_display=('user','certification_name','institution','passout_date','certificate')
class OTPAdmin(admin.ModelAdmin):  # Inherit Django's default UserAdmin
    model = OTP
    list_display = ('user','otp','created_at')

class JobAdmin(admin.ModelAdmin):
    model=Job
    list_display=('id','is_active','title','email_address','company','about_company','logo','job_description','vacancy_total','skills','required_education','location','min_salary','max_salary','job_type','office_time_from','office_time_to','employee_type')
    
class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
        fields = '__all__'

class ApplicationAdmin(admin.ModelAdmin):
    class Meta:
        model = Application
        fields = '__all__'
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP, OTPAdmin)
admin.site.register(Job,JobAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Application,ApplicationAdmin)
admin.site.register(Education,EducationAdmin)
admin.site.register(Certification,CertificationAdmin)