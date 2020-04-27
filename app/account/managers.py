from django.contrib.auth.models import BaseUserManager


class CustomUserManger(BaseUserManager):
    """
    Creates and saves a User with the given email, first name, last name
    and password.
    """

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Creates and saves a User with the given email, first name,
        last name, and password
        """
        if not email:
            raise ValueError("Users must have an email addres")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email, first name,
        last name, and password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, first_name, last_name, password, **extra_fields)
