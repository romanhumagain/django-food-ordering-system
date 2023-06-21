'''from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user.

        :param email: The email address of the user.
        :param password: The password for the user.
        :param extra_fields: Additional fields for the user.
        :return: The created user instance.
        """
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser.

        :param email: The email address of the superuser.
        :param password: The password for the superuser.
        :param extra_fields: Additional fields for the superuser.
        :return: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        return self.create_user(email, password, **extra_fields)
'''