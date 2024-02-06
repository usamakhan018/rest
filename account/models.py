from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class Contact(models.Model):
	user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followed_by", on_delete=models.CASCADE)
	user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followed", on_delete=models.CASCADE)
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user_from} follows {self.user_to}"

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
	first_name = models.CharField(max_length=255, null=True, blank=True, default="")
	last_name = models.CharField(max_length=255, null=True, blank=True, default="")
	profile_image = models.ImageField(upload_to=profile_image_path, default=default_profile_image, null=True, blank=True)
	hide_email = models.BooleanField(default=True)
	following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", symmetrical=False, through=Contact)
	
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

	def get_full_name(self):
		return f"{self.first_name} {self.last_name}"