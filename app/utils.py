import random
from django.core.mail import send_mail
from .models import OTP
from django.utils import timezone
from datetime import timedelta

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user):
    otp = generate_otp()
    OTP.objects.create(user=user, otp=otp)

    send_mail(
        f"<h1>{otp}</h1>",
        f"Your OTP code is {otp}. It is valid for 5 minutes.",
        "noreply@jobportal.com",
        [user.email],
        fail_silently=False,
    )


def delete_old_otps():
    # Get the current time
    current_time = timezone.now()
    
    # Calculate the cutoff time (e.g., 5 minutes ago)
    cutoff_time = current_time - timedelta(minutes=5)
    
    # Delete OTPs that are older than the cutoff time and are not used
    OTP.objects.filter(created_at__lt=cutoff_time, is_used=False).delete()
