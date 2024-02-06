from django.contrib.auth.tokens import PasswordResetTokenGenerator
class TokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (str(user.pk) + str(user.is_active) +str(timestamp)+ str(user.last_login))

activation_token = TokenGenerator()
