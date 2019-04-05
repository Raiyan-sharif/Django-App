from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import (UserModel, PlayerModel, ClubModel, GoverningBody)
User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    print('UserAdminCreationForm')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'phone_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    print('UserAdminCreationForm')
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'phone_number', 'password', 'active', 'is_superuser', 'staff', 'user_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class PlayerRegistrationForm(forms.ModelForm):
    class Meta:
        model = PlayerModel
        fields = ['date_of_birth', 'nationality', 'gender', 'profile_pic', 'marital_status', 'gameFrequency', 'address']


class UserProfileUpdate(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'phone_number']


class ClubRegistrationForm(forms.ModelForm):
    class Meta:
        model = ClubModel
        fields = ['club_starting_date', 'number_of_tables', 'profile_pic', 'address']


class GoverningBodyForm(forms.ModelForm):
    class Meta:
        model = GoverningBody
        fields = ['profile_pic', 'root_parent']


class UserRegistrationForm(forms.ModelForm):
    print('User Reg Form')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'phone_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    print('login')
    username = forms.CharField(label='User Name', error_messages={'required': "Enter User Name"},
                               widget=forms.TextInput(attrs={'placeholder': 'UserName'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=True,attrs={'placeholder': 'Password'}),
                               error_messages={'required': "Enter password"})





