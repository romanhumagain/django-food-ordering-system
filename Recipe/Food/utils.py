from django.core.mail import send_mail , EmailMessage
from django.conf import settings
def send_mail(email , message):
  try:
    email =EmailMessage(
        subject='Verification Required',
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
      )
  except Exception as e:
    print(str(e))
  
  