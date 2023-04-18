from django import forms
from django.forms import ModelForm, modelformset_factory


from .models import (
    SiteConfig,
    StudentClass,
    Subject,
)

SiteConfigForm = modelformset_factory(
    SiteConfig,
    fields=(
        "key",
        "value",
    ),
    extra=0,
)


class SubjectForm(ModelForm):
    prefix = "Subject"

    class Meta:
        model = Subject
        fields = ["name"]


class StudentClassForm(ModelForm):
    prefix = "Class"

    class Meta:
        model = StudentClass
        fields = ["name"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)
