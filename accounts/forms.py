from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import User, Team
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'timezone')
    def __init__(self, *args, **kwargs):
      self.request = kwargs.pop('request', None)
      return super(ProfileForm, self).__init__(*args, **kwargs)


class TeamForm(forms.ModelForm):
    name = forms.CharField(min_length=2, max_length=50)
    description = forms.CharField(min_length=10, max_length=150)
    banner_img = forms.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = Team
        fields = ('name', "description", 'banner_img')

class DeleteTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)
    
    def __init__(self, *args, **kwargs):
      self.request = kwargs.pop('request', None)
      return super(DeleteTeamForm, self).__init__(*args, **kwargs)
