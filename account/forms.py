from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import OtpCode, User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "full_name",
            "birth_date",
            "gender",
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password2"] and cd["password1"] != cd["password2"]:
            raise ValidationError("passwords dont match")
        return cd["password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href="../password/">this form</a>.'
    )

    class Meta:
        model = User
        fields = ("email", "phone_number", "full_name", "password", "last_login")


class UserRegisterForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This email already exists")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        check = User.objects.filter(phone_number=phone_number)
        if check.exists():
            raise ValidationError("")
        OtpCode.objects.filter(phone_number=phone_number).delete()
        return phone_number


class VerifyCodeForm(forms.Form):
    code = forms.CharField()


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(validators=[])
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['gender'].choices.insert(0, ('asdfasdf', 'انتخاب کنید'))

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "full_name",
            "birth_date",
            "gender",
        )
        labels = {
            "email": "ایمیل",
            "phone_number": "شماره تماس",
            "full_name": "نام و نام حانوادگی",
            "birth_date": "تاریخ تولد",
            "gender": "جنسیت",
        }


class AdminForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "ایمیل"
        self.fields['phone_number'].label = "شماره تماس"
        self.fields['full_name'].label = "نام و نام خانوادگی"
        self.fields['birth_date'].label = "تاریخ تولد"
        self.fields['gender'].label = "جنسیت"
        self.fields['password1'].label = "رمز عبور"
        self.fields['password2'].label = "تکزاز رمز عبور"
        # self.fields['gender'].empty_label = "انتخاب کنید"
