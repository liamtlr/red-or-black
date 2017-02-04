from django import forms
from rob.modeldir.models import Game, Selection
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class SelectionForm(forms.ModelForm):

    CHOICES = ('red', 'black')

    stake = forms.IntegerField(required=True)
    choice = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta:
        model = Selection
        fields = ('choice', 'stake',)
        # labels = {
        #     'body': ('Your thoughts'),
        # }
