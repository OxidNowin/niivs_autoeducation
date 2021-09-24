from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Subdivision 

from string import ascii_letters, digits

class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = r'%Y-%m-%d'


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    receipt = forms.DateField(
        label='Дата приёма',
        required=True,
        widget=MyDateInput({'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'subdivision', 'education', 'education_profile', 'receipt', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        else:
            user.set_password(
                User.objects.make_random_password(
                    length=12)
            )
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    #password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'