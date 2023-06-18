from django.core.mail import send_mail
from django.conf import settings
def send_verification(email , token):
  try:
    send_mail(
      'Verification Required',
      f'click here to verify your account: http://127.0.0.1:8000/verify/{token}',
      settings.EMAIL_HOST_USER,
      [email],
      fail_silently=False,
    )
  except Exception as e:
    return False
  
  return True