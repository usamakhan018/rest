from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
class AccountManager(BaseUserManager):
	def create_user(self, username, password):
		if not username:
			raise ValueError('Username is required')
		user = self.model(username=username)
		user.set_password(password)
		user.save()
		return user


	def create_superuser(self, username, password):
		user = self.create_user(username, password)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save()
		return user

def profile_image_path(self, filename):
	return f"profile_images/{self.pk}/"
def default_profile_image():
	return "profile_images/default_profile_image.png"

class Account(AbstractBaseUser):
	username = models.CharField(max_length=255, unique=True)
	email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
	first_name = models.CharField(max_length=255, null=True, blank=True)
	last_name = models.CharField(max_length=255, null=True, blank=True)
	profile_image = models.ImageField(upload_to=profile_image_path, default=default_profile_image, null=True, blank=True)
	hide_email = models.BooleanField(default=True)

	last_login = models.DateTimeField(auto_now=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	user_permissions = models.ManyToManyField(to="auth.permission", blank=True)
	groups = models.ManyToManyField(to="auth.group", blank=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	objects = AccountManager()

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True
