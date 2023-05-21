from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Parolayı Doğrula", widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')


        emailcheck = User.objects.filter(email=email)
        user = User.objects.filter(username=username)

        if emailcheck:
            raise forms.ValidationError("Kayıtlı Email")

        if user:
            raise forms.ValidationError("Kayıtlı Kullanıcı")

        if password != confirm:
            raise forms.ValidationError("Şifre Hatası")

        return cleaned_data








class LoginForm(forms.Form):
    username = forms.CharField(label="Email veya Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput)


    def clean_username(self):
        username=self.cleaned_data['username']

        if '@' in username:
            user = User.objects.filter(email=username)

            if len(user) == 1 :
                user = user.first()
                return user.username
            elif len(user) > 1 :
                raise forms.ValidationError('Tekrar Deneyin')

            else:
                raise forms.ValidationError('Böyle Bir Kullanıcı Yok')


        return username

