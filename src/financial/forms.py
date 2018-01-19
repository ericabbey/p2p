from django import forms
from django.contrib.auth.models import User
from dashboard.models import user_info
from .models import Transaction


class WalletForm(forms.Form):
    password = forms.CharField()
    address = forms.CharField()

    def clean(self, *args, **kwargs):
        address = self.cleaned_data.get("address")
        password = self.cleaned_data.get("password")
        if address and password:
            valid = User.check_password(password)
            print(valid)
            if not valid:
                raise forms.ValidationError(
                    "The password is incorrect"
                )
        return super(WalletForm, self).clean(*args, **kwargs)


class ProofData(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'image_proof',
            'text_proof'
        ]