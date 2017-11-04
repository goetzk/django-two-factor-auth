
class BackupTokenForm(AuthenticationTokenForm):
    otp_token = forms.CharField(label=_("Token"))

