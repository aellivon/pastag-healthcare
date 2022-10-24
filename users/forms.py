from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)


class UserLogInForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    user = None

    def clean(self, *args, **kwargs):
        # Call the parent clean here, we need this custom clean to be the last one
        super(UserLogInForm, self).clean(*args, **kwargs)
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:

            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Incorrect email or password!")

            # Lets the user know that this email is inactive
            if not user.is_active:
                raise forms.ValidationError("This email has been deactivated!")

            # All looks well. Assign the user to our form's user
            self.user = user
        return self.cleaned_data


class AccountForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']