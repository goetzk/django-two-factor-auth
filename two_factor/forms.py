from binascii import unhexlify
from time import time

from django import forms
from django.forms import Form, ModelForm
from django.utils.translation import ugettext_lazy as _
from django_otp.forms import OTPAuthenticationFormMixin

from .models import get_available_methods
from .utils import totp_digits


class MethodForm(forms.Form):
    method = forms.ChoiceField(label=_("Method"),
                               initial='generator',
                               widget=forms.RadioSelect)

    def __init__(self, **kwargs):
        super(MethodForm, self).__init__(**kwargs)
        self.fields['method'].choices = get_available_methods()



class DeviceValidationForm(forms.Form):
    token = forms.IntegerField(label=_("Token"), min_value=1, max_value=int('9' * totp_digits()))

    error_messages = {
        'invalid_token': _('Entered token is not valid.'),
    }

    def __init__(self, device, **args):
        super(DeviceValidationForm, self).__init__(**args)
        self.device = device

    def clean_token(self):
        token = self.cleaned_data['token']
        if not self.device.verify_token(token):
            raise forms.ValidationError(self.error_messages['invalid_token'])
        return token


class DisableForm(forms.Form):
    understand = forms.BooleanField(label=_("Yes, I am sure"))


class AuthenticationTokenForm(OTPAuthenticationFormMixin, Form):
    otp_token = forms.IntegerField(label=_("Token"), min_value=1,
                                   max_value=int('9' * totp_digits()))

    otp_token.widget.attrs.update({'autofocus': 'autofocus'})

    # Our authentication form has an additional submit button to go to the
    # backup token form. When the `required` attribute is set on an input
    # field, that button cannot be used on browsers that implement html5
    # validation. For now we'll use this workaround, but an even nicer
    # solution would be to move the button outside the `<form>` and into
    # its own `<form>`.
    use_required_attribute = False

    def __init__(self, user, initial_device, **kwargs):
        """
        `initial_device` is either the user's default device, or the backup
        device when the user chooses to enter a backup token. The token will
        be verified against all devices, it is not limited to the given
        device.
        """
        super(AuthenticationTokenForm, self).__init__(**kwargs)
        self.user = user

        # YubiKey generates a OTP of 44 characters (not digits). So if the
        # user's primary device is a YubiKey, replace the otp_token
        # IntegerField with a CharField.
        if RemoteYubikeyDevice and YubikeyDevice and \
                isinstance(initial_device, (RemoteYubikeyDevice, YubikeyDevice)):
            self.fields['otp_token'] = forms.CharField(label=_('YubiKey'))

    def clean(self):
        self.clean_otp(self.user)
        return self.cleaned_data


