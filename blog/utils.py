import random
import string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

def random_string_generater(size=10,chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return(
            six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.profile.email_confirmed)
            )
account_activation_token = AccountActivationTokenGenerator()