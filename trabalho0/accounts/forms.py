from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Senha',
        min_length=8,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirmar Senha',
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        labels = {
            'name': 'Nome',
            'email': 'E-mail',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail', widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ['username', 'password']
