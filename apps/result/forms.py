from django import forms
from django.forms import modelformset_factory

from apps.corecode.models import Subject

from .models import Result


class CreateResults(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )


EditResults = modelformset_factory(
    Result, fields=("test_score", "exam_score"), extra=0, can_delete=True
)
