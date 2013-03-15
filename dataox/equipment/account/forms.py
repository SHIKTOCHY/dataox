import account.forms
from django import forms
import account.models

class SignupForm(account.forms.SignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    good_domains = frozenset(['ouh.nhs.uk'])

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields["username"]
        self.fields.keyOrder = ('first_name', 'last_name', 'email', 'password', 'password_confirm')

    def clean_email(self):
        email = super(SignupForm, self).clean_email()
        domain = email.rsplit('@', 1)[-1]
        if domain not in self.good_domains:
            raise forms.ValidationError('Registrations from your email domain are not permitted.')
        return self.cleaned_data['email']