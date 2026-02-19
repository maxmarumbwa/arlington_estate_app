from django import forms
from .models import PropertyReport


class PropertyReportForm(forms.ModelForm):
    class Meta:
        model = PropertyReport
        fields = [
            "house_number",
            "latitude",
            "longitude",
            "violation",
            "description",
        ]

        widgets = {
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }
